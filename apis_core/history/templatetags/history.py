from django import template
from django.utils.safestring import mark_safe

from apis_core.history.serializers import HistoryLogSerializer
from apis_core.history.utils import triple_sidebar_history
from apis_core.utils.helpers import get_html_diff

register = template.Library()


@register.simple_tag(takes_context=True)
def object_relations_history(context, detail=True):
    obj = context["object"]
    return triple_sidebar_history(obj, context["request"], detail)


@register.filter
def get_history_data(obj):
    data = HistoryLogSerializer(obj.get_history_data(), many=True).data
    return data


@register.filter
def get_diff_old(change, shorten=0):
    return mark_safe(get_html_diff(a=change.old, b=change.new, show_b=False))


@register.filter
def get_diff_new(change, shorten=0):
    return mark_safe(get_html_diff(a=change.old, b=change.new, show_a=False))
