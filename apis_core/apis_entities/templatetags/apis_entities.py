from django import template
from django.contrib.contenttypes.models import ContentType

from apis_core.apis_entities.models import AbstractEntity
from apis_core.apis_entities.utils import get_entity_classes

register = template.Library()


@register.simple_tag
def url_replace(request, field, value):
    dict_ = request.GET.copy()
    dict_[field] = value

    return dict_.urlencode()


def is_entity(content_type: ContentType):
    model_class = content_type.model_class()
    return model_class is not None and issubclass(model_class, AbstractEntity)


@register.simple_tag
def entities_content_types():
    """
    Retrieve all models which inherit from AbstractEntity class
    and return their ContentType.
    """
    entities = list(
        filter(
            lambda content_type: is_entity(content_type),
            ContentType.objects.all(),
        )
    )
    return entities


@register.simple_tag
def entities_verbose_name_plural_listview_url():
    """
    Return all entities verbose names together with their list uri, sorted in alphabetical order
    USED BY:
    * `core/base.html`
    """
    ret = {
        entity._meta.verbose_name_plural: entity.get_listview_url()
        for entity in get_entity_classes()
    }
    return sorted(ret.items())
