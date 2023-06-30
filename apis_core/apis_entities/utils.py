import functools
from django.contrib.contenttypes.models import ContentType
from apis_core.apis_entities.models import AbstractEntity
from apis_core.utils.settings import get_entity_settings


@functools.cache
def list_entity_contenttypes():
    cts = ContentType.objects.all()
    cts = filter(lambda ct: ct.model_class(), cts)
    cts = filter(lambda ct: issubclass(ct.model_class(), AbstractEntity), cts)
    cts = filter(lambda ct: ct.app_label != "apis_entities", cts)
    return list(cts)


@functools.cache
def list_entity_listviews():
    ects = list_entity_contenttypes()
    ects = filter(lambda ect: not get_entity_settings(ect.model).get('menuexclude', False), ects)
    return [e.model_class() for e in ects]
