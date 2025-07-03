import functools
import logging

from django.conf import settings
from django.contrib.auth import get_permission_codename
from django.db.models import CharField, Model, Q, TextField
from django.utils import module_loading

logger = logging.getLogger(__name__)


def default_search_fields(model, field_names=None):
    """
    Retrieve the default model fields to use for a search operation
    By default those are all the CharFields and TextFields of a model.
    It is also possible to define those fields on the model using the
    `_default_search_fields` attribute.
    The method also takes a `field_names` argument to override the list
    of fields.
    """
    default_types = (CharField, TextField)
    fields = [
        field for field in model._meta.get_fields() if isinstance(field, default_types)
    ]
    # check if the model has a `_default_search_fields`
    # list and use that as searchfields
    if isinstance(getattr(model, "_default_search_fields", None), list):
        fields = [
            model._meta.get_field(field) for field in model._default_search_fields
        ]
    # if `fields_to_search` is a list, use that
    if isinstance(field_names, list):
        fields = [model._meta.get_field(field) for field in field_names]
    return fields


def generate_search_filter(model, query, fields_to_search=None, prefix=""):
    """
    Generate a default search filter that searches for the `query`
    This helper can be used by autocomplete querysets if nothing
    fancier is needed.
    If the `prefix` is set, the field names will be prefixed with that string -
    this can be useful if you want to use the `generate_search_filter` in a
    `Q` combined query while searching over multiple models.
    """
    if isinstance(query, str):
        query = query.split()

    _fields_to_search = [
        field.name for field in default_search_fields(model, fields_to_search)
    ]

    q = Q()

    for token in query:
        q &= functools.reduce(
            lambda acc, field_name: acc
            | Q(**{f"{prefix}{field_name}__icontains": token}),
            _fields_to_search,
            Q(),
        )
    return q


@functools.lru_cache
def mro_paths(model):
    """
    Create a list of MRO classes for a Django model
    """
    paths = []
    if model is not None:
        for cls in filter(lambda x: x not in Model.mro(), model.mro()):
            paths.append(tuple([cls.__module__.split(".")[-2], cls.__name__]))
            paths.append(tuple(cls.__module__.split(".")[:-1] + [cls.__name__]))
    return [list(path) for path in list(dict.fromkeys(paths))]


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
    prepends = []
    for prepend in getattr(settings, "ADDITIONAL_MODULE_LOOKUP_PATHS", []):
        prepends.extend(
            list(map(lambda x: prepend.split(".") + [path] + x[-1:], mro_paths(model)))
        )
    classes = tuple(".".join(prefix) + suffix for prefix in prepends + paths)
    return classes


@functools.lru_cache
def makeclassprefix(string: str) -> str:
    string = "".join([c if c.isidentifier() else " " for c in string])
    string = "".join([word.strip().capitalize() for word in string.split(" ")])
    return string


@functools.lru_cache
def import_string(dotted_path):
    try:
        return module_loading.import_string(dotted_path)
    except (ModuleNotFoundError, ImportError) as e:
        logger.debug("Could not load %s: %s", dotted_path, e)
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


def split_and_strip_parameter(params: [str]) -> [str]:
    """
    Clean a URI param list type
    This method iterates through a list of strings. It looks if
    the items contain a comma separated list of items and then splits
    those and also runs strip on all those items.
    So out of ["foo.bar", "bar.faz, faz.foo"] it
    creates a list ["foo.bar", "bar.faz", "faz.foo"]
    """
    newlist = []
    for param in params:
        subparams = map(str.strip, param.split(","))
        newlist.extend(subparams)
    return newlist


def string_to_bool(string: str = "false") -> bool:
    """
    Convert a string to a boolean representing its semantic value
    """
    return string.lower() == "true"
