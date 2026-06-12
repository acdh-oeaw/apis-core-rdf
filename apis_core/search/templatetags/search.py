from functools import cache

from django import template
from django.contrib.contenttypes.models import ContentType

register = template.Library()


@register.filter(name="id_to_content_type")
@cache
def id_to_content_type(value):
    return ContentType.objects.get(pk=value)
