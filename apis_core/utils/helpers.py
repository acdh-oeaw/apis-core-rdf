import functools
import importlib
import inspect
import itertools
import logging

from django.http import Http404
from django.apps import apps
from django.db import DEFAULT_DB_ALIAS, router
from django.contrib.contenttypes.models import ContentType
from django.core import serializers

#########################################################
# Some of these methods are used on startup of the Django
# application, because they are referenced in models.
# Therefore we have to put the imports of models into the
# method bodies, so we don't get circular imports.
# In the long run we might look into removing the need for
# importing those functions in the model classes
###########################################################


@functools.lru_cache
def get_classes_with_allowed_relation_from(entity_name: str) -> list:
    """Returns a list of classes to which the given class may be related by a Property"""
    from apis_core.apis_relations.models import Property

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


APIS_APP_LABELS = [
    "apis_metainfo",
    "apis_relations",
    "apis_vocabularies",
    "apis_entities",
]


@functools.cache
def get_apis_model_classes():
    """
    Get all model classes that are part of the apis core modules. We do this
    by getting all the models from all the apps and comparing their app_labels
    """
    model_classes = filter(
        lambda model: model._meta.label_lower.split(".")[0] in APIS_APP_LABELS,
        apps.get_models(),
    )
    return list(model_classes)


@functools.cache
def get_entities_model_classes():
    """
    Get all model classes that are part of ontologies modules. We do this
    by getting all the models from all the apps and checking which of them
    inherit from `AbstractEntity`. Then we also remove `TempEntityClass`.
    """
    from apis_core.apis_entities.models import AbstractEntity, TempEntityClass

    model_classes = list(
        filter(lambda model: issubclass(model, AbstractEntity), apps.get_models())
    )
    model_classes.remove(TempEntityClass)
    return model_classes


@functools.cache
def get_entity_class_by_name(name: str):
    """
    This is sometimes needed in the code to get a class by a human readable
    identifier (`person`, `place`, ...). In various cases is would be probably
    better to use the ContentTypes framework instead
    """
    for entity in get_entities_model_classes():
        _, model_name = entity._meta.label_lower.split(".")
        if model_name == name.lower():
            return entity
    raise Http404(f"Entity {entity} not found.")


@functools.cache
def property_autocomplete_choices(entity_name_from, entity_name_to, needle):
    from apis_core.apis_entities.autocomplete3 import PropertyAutocomplete
    from apis_core.apis_relations.models import Property

    model_from = ContentType.objects.get_for_model(
        get_entity_class_by_name(entity_name_from)
    )
    model_to = ContentType.objects.get_for_model(
        get_entity_class_by_name(entity_name_to)
    )

    rbc_self_subj_other_obj = Property.objects.filter(
        subj_class=model_from,
        obj_class=model_to,
        name__icontains=needle,
    )
    rbc_self_obj_other_subj = Property.objects.filter(
        subj_class=model_to,
        obj_class=model_from,
        name_reverse__icontains=needle,
    )
    choices = []
    # The Select2ListView class when finding results for some user input, returns these
    # results in this 'choices' list. This is a list of dictionaries, where each dictionary
    # has an id and a text. In our case however the results can come from two different sets:
    # the one where result hits match on the forward name of a property and the other set
    # where the result hits match on the reverse name. These hits need to re-used later,
    # but additionally the direction of the property is also needed later to persist it
    # correctly (e.g. when creating a triple between two persons, where one is the mother and
    # the other is the daughter, then the property direction is needed). I could not find a
    # way to return in this function a choices list with dictionaries or something else,
    # that would pass additional data. So I am misusing the 'id' item in the dictionary by
    # encoding the id and the direction into a string which will be parsed and split later on.
    for rbc in rbc_self_subj_other_obj:
        choices.append(
            {
                # misuse of the id item as explained above
                "id": f"id:{rbc.pk}__direction:{PropertyAutocomplete.SELF_SUBJ_OTHER_OBJ_STR}",
                "text": rbc.name,
            }
        )
    for rbc in rbc_self_obj_other_subj:
        choices.append(
            {
                # misuse of the id item as explained above
                "id": f"id:{rbc.pk}__direction:{PropertyAutocomplete.SELF_OBJ_OTHER_SUBJ_STR}",
                "text": rbc.name_reverse,
            }
        )
    return choices


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
