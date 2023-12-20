import functools
import importlib
import inspect
import itertools
import logging
from typing import Type


from apis_core.apis_relations.models import Property, TempTriple
from apis_core.utils.settings import get_entity_settings_by_modelname
from apis_core.apis_relations.tables import get_generic_triple_table

from django.apps import apps
from django.db import DEFAULT_DB_ALIAS, router
from django.db.models import Q
from django.contrib.contenttypes.models import ContentType
from django.core import serializers
from django_tables2 import RequestConfig


@functools.lru_cache
def get_classes_with_allowed_relation_from(
    entity_name: str,
) -> list[object]:
    """Returns a list of classes to which the given class may be related by a Property"""

    # Find all the properties where the entity is either subject or object
    properties_with_entity_as_subject = Property.objects.filter(
        subj_class__model=entity_name
    ).prefetch_related("obj_class")
    properties_with_entity_as_object = Property.objects.filter(
        obj_class__model=entity_name
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
    return [
        content_type.model_class()
        for content_type in set(itertools.chain(*content_type_querysets))
    ]


def get_member_for_entity(
    model: object, suffix: str = None, path: str = None
) -> object:
    """
    Look for a module memeber whose name and location are derived from a Django model,
    a suffix and optinally a path. The name is derived from the modelname and the suffix.
    The location is derived from the models app_name and the path. If no path is
    given, a default path is generated by using the suffix + "s".
    So for example with a model `apis_ontology.Person` and suffix `Table` it returns
    `apis_ontology.tables.PersonTable` if it exists. If it does not find a matching member, it
    returns None. If we add the path "mytables" it looks for the member
    `apis_ontology.mytables.PersonTable`.
    """
    ct = ContentType.objects.get_for_model(model)
    module = ct.app_label
    model = ct.model.capitalize()
    if suffix:
        model += suffix
    if path:
        module += f".{path}"
    else:
        if suffix:
            module += f".{suffix.lower()}s"
    logging.debug("Checking if %s.%s exists", module, model)
    try:
        members = inspect.getmembers(importlib.import_module(module))
        members = list(filter(lambda c: c[0] == model, members))
    except ModuleNotFoundError:
        members = []
    if members:
        logging.debug("Found %s.%s", module, model)
        return members[0][1]
    return None


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


def triple_sidebar(pk: int, entity_name: str, request, detail=True):
    side_bar = []

    triples_related_all = (
        TempTriple.objects_inheritance.filter(Q(subj__pk=pk) | Q(obj__pk=pk))
        .all()
        .select_subclasses()
    )

    for entity_class in get_classes_with_allowed_relation_from(entity_name):
        entity_content_type = ContentType.objects.get_for_model(entity_class)

        other_entity_class_name = entity_class.__name__.lower()

        triples_related_by_entity = triples_related_all.filter(
            (Q(subj__self_contenttype=entity_content_type) & Q(obj__pk=pk))
            | (Q(obj__self_contenttype=entity_content_type) & Q(subj__pk=pk))
        )

        table_class = get_generic_triple_table(
            other_entity_class_name=other_entity_class_name,
            entity_pk_self=pk,
            detail=detail,
        )

        prefix = f"{other_entity_class_name}"
        title_card = prefix
        tb_object = table_class(data=triples_related_by_entity, prefix=prefix)
        tb_object_open = request.GET.get(prefix + "page", None)
        entity_settings = get_entity_settings_by_modelname(entity_class.__name__)
        per_page = entity_settings.get("relations_per_page", 10)
        RequestConfig(request, paginate={"per_page": per_page}).configure(tb_object)
        tab_id = f"triple_form_{entity_name}_to_{other_entity_class_name}"
        side_bar.append(
            (
                title_card,
                tb_object,
                tab_id,
                tb_object_open,
            )
        )
    return side_bar
