import difflib
import itertools

from django.apps import apps
from django.contrib.contenttypes.models import ContentType
from django.core import serializers
from django.core.exceptions import ImproperlyConfigured
from django.db import DEFAULT_DB_ALIAS, router
from django.db.models import Q
from django_tables2 import RequestConfig

from apis_core.apis_metainfo.models import Uri
from apis_core.apis_relations.models import Property, TempTriple
from apis_core.apis_relations.tables import get_generic_triple_table
from apis_core.generic.helpers import first_member_match, module_paths
from apis_core.utils.settings import get_entity_settings_by_modelname


def get_content_types_with_allowed_relation_from(
    content_type: ContentType,
) -> list[ContentType]:
    """Returns a list of ContentTypes to which the given ContentTypes may be related by a Property"""

    # Find all the properties where the entity is either subject or object
    properties_with_entity_as_subject = Property.objects.filter(
        subj_class=content_type
    ).prefetch_related("obj_class")
    properties_with_entity_as_object = Property.objects.filter(
        obj_class=content_type
    ).prefetch_related("subj_class")

    content_type_querysets = []

    # Where entity is subject, get all the object content_types
    for p in properties_with_entity_as_subject:
        objs = p.obj_class.all()
        content_type_querysets.append(objs)
    # Where entity is object, get all the subject content_types
    for p in properties_with_entity_as_object:
        subjs = p.subj_class.all()
        content_type_querysets.append(subjs)

    # Join querysets with itertools.chain, call set to make unique, and extract the model class
    return set(itertools.chain(*content_type_querysets))


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


def triple_sidebar(obj: object, request, detail=True):
    content_type = ContentType.objects.get_for_model(obj)
    side_bar = []

    triples_related_all = (
        TempTriple.objects_inheritance.filter(Q(subj__pk=obj.pk) | Q(obj__pk=obj.pk))
        .all()
        .select_subclasses()
    )

    for other_content_type in get_content_types_with_allowed_relation_from(
        content_type
    ):
        triples_related_by_entity = triples_related_all.filter(
            (Q(subj__self_contenttype=other_content_type) & Q(obj__pk=obj.pk))
            | (Q(obj__self_contenttype=other_content_type) & Q(subj__pk=obj.pk))
        )

        table_class = get_generic_triple_table(
            other_entity_class_name=other_content_type.model,
            entity_pk_self=obj.pk,
            detail=detail,
        )

        prefix = f"{other_content_type.model}"
        title_card = other_content_type.name
        tb_object = table_class(data=triples_related_by_entity, prefix=prefix)
        tb_object_open = request.GET.get(prefix + "page", None)
        entity_settings = get_entity_settings_by_modelname(content_type.model)
        per_page = entity_settings.get("relations_per_page", 10)
        RequestConfig(request, paginate={"per_page": per_page}).configure(tb_object)
        tab_id = f"triple_form_{content_type.model}_to_{other_content_type.model}"
        side_bar.append(
            (
                title_card,
                tb_object,
                tab_id,
                tb_object_open,
            )
        )
    return side_bar


def get_importer_for_model(model: object):
    importer_paths = module_paths(model, path="importers", suffix="Importer")
    if importer := first_member_match(importer_paths):
        return importer
    raise ImproperlyConfigured(f"No suitable importer found for {model}")


def create_object_from_uri(uri: str, model: object) -> object:
    if uri.startswith("http"):
        try:
            uri = Uri.objects.get(uri=uri)
            return uri.root_object
        except Uri.DoesNotExist:
            Importer = get_importer_for_model(model)
            importer = Importer(uri, model)
            instance = importer.create_instance()
            uri = Uri.objects.create(uri=importer.get_uri, root_object=instance)
            return instance
    return None


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
