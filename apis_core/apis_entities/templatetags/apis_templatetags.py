from operator import itemgetter
from django import template
from apis_core.utils import caching
from apis_core.utils.helpers import triple_sidebar
from django.contrib.contenttypes.models import ContentType
from apis_core.apis_entities.models import AbstractEntity

from apis_core.apis_entities.utils import get_entity_classes

register = template.Library()


@register.simple_tag
def url_replace(request, field, value):
    dict_ = request.GET.copy()
    dict_[field] = value

    return dict_.urlencode()


@register.simple_tag
def entities_list_links():
    """
    Retrieve all models which inherit from AbstractEntity class
    and return their class name and verbose name.
    """
    entities_classes = caching.get_all_entity_classes() or []
    entities_links = [
        (e.__name__.lower(), e._meta.verbose_name.title()) for e in entities_classes
    ]
    entities_links.sort(key=itemgetter(1))

    return entities_links


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


@register.simple_tag(takes_context=True)
def object_relations(context, detail=True):
    obj = context["object"]
    return triple_sidebar(
        obj.pk, obj.__class__.__name__.lower(), context["request"], detail
    )
