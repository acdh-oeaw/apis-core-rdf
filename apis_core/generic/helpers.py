import functools
import logging

from django.contrib.auth import get_permission_codename
from django.db.models import CharField, Model, Q, TextField
from django.utils import module_loading

logger = logging.getLogger(__name__)


def generate_search_filter(model, query, fields_to_search=None, prefix=""):
    """
    Generate a default search filter to look for a string in a number of
    a model's fields.

    Can be used by e.g. autocomplete QuerySets if nothing fancier is needed.

    The fields whose values are searched are (in order of precedence):
        * all of a model's CharFields and TextFields (excluding
          ArrayField base_fields),
        * defined on the model using the attribute `_default_search_fields`,
        * passed in via `fields_to_search`.
    When set explicitly, a list of (string-formatted) field names is expected.

    :param model: name of the model to run the filter on
    :type model: str
    :param query: the search string
    :type query: str
    :param fields_to_search: a list of field names (strings)
    :type fields_to_search: list
    :param prefix: optional prefix for field names; may be helpful for
                   searching over multiple models using `Q`-combined queries
    :type prefix: str
    :return: a Q() object
    :rtype: django.db.models.query_utils.Q
    """
    query = query.split()

    modelfields = model._meta.fields
    # search all model fields of type CharField, TextField
    _fields_to_search = [
        field.name for field in modelfields if isinstance(field, (CharField, TextField))
    ]

    # ... unless model attribute `_default_search_fields` of type list is set
    if isinstance(getattr(model, "_default_search_fields", None), list):
        _fields_to_search = model._default_search_fields

    # ... unless method is called with argument `fields_to_search` of type list
    if isinstance(fields_to_search, list):
        _fields_to_search = fields_to_search

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
def makeclassprefix(string: str) -> str:
    string = "".join([c if c.isidentifier() else " " for c in string])
    string = "".join([word.strip().capitalize() for word in string.split(" ")])
    return string


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
