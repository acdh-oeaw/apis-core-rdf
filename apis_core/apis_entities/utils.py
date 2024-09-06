from django.apps import apps

from apis_core.apis_entities.models import AbstractEntity


def get_entity_classes():
    return list(filter(lambda x: issubclass(x, AbstractEntity), apps.get_models()))
