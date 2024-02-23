from operator import itemgetter
from django import template
from apis_core.utils import caching
from apis_core.utils.helpers import get_classes_with_allowed_relation_from

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


@register.filter
def triple_form_types(instance):
    """
    This is a helper function to generate identifiers which
    are then used in `abstractentity_form.html` in the javascript
    part to initialize the old triple tables and forms.
    """
    entity_name = instance._meta.verbose_name
    object_relations = []
    for entity_class in get_classes_with_allowed_relation_from(entity_name):
        other_entity_class_name = entity_class.__name__.lower()
        object_relations.append(
            f"triple_form_{entity_name}_to_{other_entity_class_name}"
        )
    return object_relations
