import functools
import inspect
import importlib
import logging

from django.db.models import CharField, TextField, Q, Model
from django.contrib.auth import get_permission_codename

logger = logging.getLogger(__name__)


def generate_search_filter(model, query, fields_to_search=None):
    """
    Generate a default search filter that searches for the `query`
    in all the CharFields and TextFields of a model (case-insensitive)
    or in the fields listed in the `fields_to_search` argument.
    This helper can be used by autocomplete querysets if nothing
    fancier is needed.
    """
    query = query.split()

    if isinstance(fields_to_search, list):
        fields_to_search = [
            field.name for field in model._meta.fields if field.name in fields_to_search
        ]
    else:
        fields_to_search = [
            field.name
            for field in model._meta.fields
            if isinstance(field, (CharField, TextField))
        ]

    q = Q()

    for token in query:
        q &= functools.reduce(
            lambda acc, field_name: acc | Q(**{f"{field_name}__icontains": token}),
            fields_to_search,
            Q(),
        )
    return q


@functools.lru_cache
def mro_paths(model):
    """
    Create a list of MRO classes for a Django model
    """
    paths = []
    for cls in filter(lambda x: x not in Model.mro(), model.mro()):
        paths.append(cls.__module__.split(".")[:-1] + [cls.__name__])
    return paths


@functools.lru_cache
def template_names_via_mro(model, suffix=""):
    """
    Use the MRO to generate a list of template names for a model
    """
    mro_prefix_list = ["/".join(prefix) for prefix in mro_paths(model)]
    return [f"{prefix.lower()}{suffix}" for prefix in mro_prefix_list]


@functools.lru_cache
def class_from_path(classpath):
    """
    Lookup if the class in `classpath` exists - if so return it,
    otherwise return False
    """
    module, cls = classpath.rsplit(".", 1)
    try:
        members = inspect.getmembers(importlib.import_module(module))
        members = list(filter(lambda c: c[0] == cls, members))
    except ModuleNotFoundError:
        return False
    if members:
        return members[0]
    return False


@functools.lru_cache
def first_match_via_mro(model, path: str = "", suffix: str = ""):
    """
    Based on the MRO of a Django model, look for classes based on a
    lookup algorithm and return the first one that matches.
    """
    paths = list(map(lambda x: x[:-1] + [path] + x[-1:], mro_paths(model)))
    classes = [".".join(prefix) + suffix for prefix in paths]
    name, res = next(filter(bool, map(class_from_path, classes)), ("nothing", None))
    logger.debug(
        "first_match_via_mro: found %s for %s, path: `%s`, suffix: `%s`",
        name,
        model,
        path,
        suffix,
    )
    return res


@functools.lru_cache
def permission_fullname(action: str, model: object) -> str:
    permission_codename = get_permission_codename(action, model._meta)
    return f"{model._meta.app_label}.{permission_codename}"
