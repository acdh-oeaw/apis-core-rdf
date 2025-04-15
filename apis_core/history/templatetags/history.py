from django import template
from django.utils.safestring import mark_safe

from apis_core.utils.helpers import get_html_diff

register = template.Library()


@register.filter
def get_diff_old(change, shorten=0):
    return mark_safe(get_html_diff(a=change.old, b=change.new, show_b=False))


@register.filter
def get_diff_new(change, shorten=0):
    return mark_safe(get_html_diff(a=change.old, b=change.new, show_a=False))
