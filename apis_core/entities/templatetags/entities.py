from django import template
from django.contrib.contenttypes.models import ContentType

from apis_core.entities.abc import Entity

register = template.Library()


def is_entity(content_type: ContentType):
    model_class = content_type.model_class()
    return model_class is not None and issubclass(model_class, Entity)


@register.simple_tag
def entities_content_types():
    """
    Retrieve all models which inherit from Entity class
    and return their ContentType.
    """
    entities = list(
        filter(
            lambda content_type: is_entity(content_type),
            ContentType.objects.all(),
        )
    )
    return entities
