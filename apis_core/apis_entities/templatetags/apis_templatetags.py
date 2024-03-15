from operator import itemgetter
from django import template
from apis_core.utils import caching
from apis_core.utils.helpers import triple_sidebar

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


@register.simple_tag(takes_context=True)
def object_relations(context, detail=True):
    obj = context["object"]
    return triple_sidebar(
        obj.pk, obj.__class__.__name__.lower(), context["request"], detail
    )
