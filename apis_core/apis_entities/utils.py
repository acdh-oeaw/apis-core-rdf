from django.apps import apps
from django.contrib.contenttypes.models import ContentType

from apis_core.apis_entities.models import AbstractEntity


def get_entity_classes():
    return list(filter(lambda x: issubclass(x, AbstractEntity), apps.get_models()))


def get_entity_content_types():
    return [ContentType.objects.get_for_model(model) for model in get_entity_classes()]
