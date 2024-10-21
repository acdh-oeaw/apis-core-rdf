from django import template

from apis_core.apis_relations.utils import triple_sidebar

register = template.Library()


@register.simple_tag(takes_context=True)
def object_relations(context, detail=True):
    obj = context["object"]
    return triple_sidebar(obj, context["request"], detail)
