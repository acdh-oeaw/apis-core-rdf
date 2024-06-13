import functools
import logging

from django.db.models import CharField, TextField, Q, Model
from django.contrib.auth import get_permission_codename
from django.utils import module_loading

logger = logging.getLogger(__name__)


def generate_search_filter(model, query, fields_to_search=None, prefix=""):
    """
    Generate a default search filter that searches for the `query`
    in all the CharFields and TextFields of a model (case-insensitive)
    or in the fields listed in the `fields_to_search` argument.
    This helper can be used by autocomplete querysets if nothing
    fancier is needed.
    If the `prefix` is set, the field names will be prefixed with that string -
    this can be useful if you want to use the `generate_search_filter` in a
    `Q` combined query while searching over multiple models.
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
            lambda acc, field_name: acc
            | Q(**{f"{prefix}{field_name}__icontains": token}),
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
def permission_fullname(action: str, model: object) -> str:
    permission_codename = get_permission_codename(action, model._meta)
    return f"{model._meta.app_label}.{permission_codename}"


@functools.lru_cache
def module_paths(model, path: str = "", suffix: str = "") -> list:
    paths = list(map(lambda x: x[:-1] + [path] + x[-1:], mro_paths(model)))
    classes = tuple(".".join(prefix) + suffix for prefix in paths)
    return classes


@functools.lru_cache
def import_string(dotted_path):
    try:
        return module_loading.import_string(dotted_path)
    except (ModuleNotFoundError, ImportError):
        return False


@functools.lru_cache
def first_member_match(dotted_path_list: tuple[str], fallback=None) -> object:
    logger.debug("Looking for matching class in %s", dotted_path_list)
    pathgen = map(import_string, dotted_path_list)
    result = next(filter(bool, pathgen), None)
    if result:
        logger.debug("Found matching attribute/class in %s", result)
    else:
        logger.debug("Found nothing, returning fallback: %s", fallback)
    return result or fallback
