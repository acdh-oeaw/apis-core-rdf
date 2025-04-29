import difflib

from django.apps import apps
from django.core import serializers
from django.core.exceptions import ImproperlyConfigured
from django.db import DEFAULT_DB_ALIAS, router

from apis_core.generic.helpers import first_member_match, module_paths


def datadump_get_objects(models: list = [], *args, **kwargs):
    for model in models:
        if not model._meta.proxy and router.allow_migrate_model(
            DEFAULT_DB_ALIAS, model
        ):
            objects = model._default_manager
            queryset = objects.using(DEFAULT_DB_ALIAS).order_by(model._meta.pk.name)
            yield from queryset.iterator()


def datadump_get_queryset(additional_app_labels: list = []):
    """
    This method is loosely based on the `dumpdata` admin command.
    It iterates throug the relevant app models and exports them using
    a serializer and natural foreign keys.
    Data exported this way can be reimported into a newly created Django APIS app
    """

    # get all APIS apps and all APIS models
    apis_app_labels = ["apis_relations", "apis_metainfo"]
    apis_app_models = [
        model for model in apps.get_models() if model._meta.app_label in apis_app_labels
    ]

    # create a list of app labels we want to iterate
    # this allows to extend the apps via the ?app_labels= parameter
    app_labels = set(apis_app_labels)
    app_labels |= set(additional_app_labels)

    # look for models that inherit from APIS models and add their
    # app label to app_labels
    for model in apps.get_models():
        if any(map(lambda x: issubclass(model, x), apis_app_models)):
            app_labels.add(model._meta.app_label)

    # now go through all app labels
    app_list = {}
    for app_label in app_labels:
        app_config = apps.get_app_config(app_label)
        app_list[app_config] = None

    models = serializers.sort_dependencies(app_list.items(), allow_cycles=True)

    yield from datadump_get_objects(models)


def datadump_serializer(additional_app_labels: list = [], serialier_format="json"):
    return serializers.serialize(
        serialier_format,
        datadump_get_queryset(additional_app_labels),
        use_natural_foreign_keys=True,
    )


def get_importer_for_model(model: object):
    importer_paths = module_paths(model, path="importers", suffix="Importer")
    if importer := first_member_match(importer_paths):
        return importer
    raise ImproperlyConfigured(f"No suitable importer found for {model}")


def get_html_diff(a, b, show_a=True, show_b=True, shorten=0):
    """
    Create an colorized html represenation of the difference of two values a and b
    If `show_a` is True, colorize deletions in `a`
    If `show_b` is True, colorize insertions in `b`
    The value of `shorten` defines if long parts of strings that contains no change should be shortened
    """

    def style_remove(text):
        return f"<span class='diff-remove'>{text}</span>"

    def style_insert(text):
        return f"<span class='diff-insert'>{text}</span>"

    nones = ["", None]
    if a in nones and b in nones:
        result = ""
    elif a in nones:
        result = style_insert(b) if show_b else ""
    elif b in nones:
        result = style_remove(a) if show_a else ""
    else:
        result = ""
        a = str(a)
        b = str(b)
        codes = difflib.SequenceMatcher(None, a, b).get_opcodes()
        for opcode, a_start, a_end, b_start, b_end in codes:
            match opcode:
                case "equal":
                    equal = a[a_start:a_end]
                    if shorten and len(equal) > shorten:
                        equal = equal[:5] + " ... " + equal[-10:]
                    result += equal
                case "delete":
                    if show_a:
                        result += style_remove(a[a_start:a_end])
                case "insert":
                    if show_b:
                        result += style_insert(b[b_start:b_end])
                case "replace":
                    if show_b:
                        result += style_insert(b[b_start:b_end])
                    if show_a:
                        result += style_remove(a[a_start:a_end])
    return result


def construct_lookup(value: str) -> tuple[str, str]:
    """
    Helper method to parse input values and construct field lookups
    (https://docs.djangoproject.com/en/4.2/ref/models/querysets/#field-lookups)
    Parses user input for wildcards and returns a tuple containing the
    interpreted django lookup string and the trimmed value
    E.g.

    - ``example`` -> ``('__icontains', 'example')``
    - ``*example*`` -> ``('__icontains', 'example')``
    - ``*example`` -> ``('__iendswith', 'example')``
    - ``example*``-> ``('__istartswith', 'example')``
    - ``"example"`` -> ``('__iexact', 'example')``

    :param str value: text to be parsed for ``*``
    :return: a tuple containing the lookup type and the value without modifiers
    """

    if value.startswith("*") and not value.endswith("*"):
        value = value[1:]
        return "__iendswith", value

    elif not value.startswith("*") and value.endswith("*"):
        value = value[:-1]
        return "__istartswith", value

    elif value.startswith('"') and value.endswith('"'):
        value = value[1:-1]
        return "__iexact", value

    else:
        if value.startswith("*") and value.endswith("*"):
            value = value[1:-1]
        return "__icontains", value


def flatten_if_single(value: list):
    if len(value) == 1:
        return value[0]
    return value
