from django import template
from django.conf import settings


register = template.Library()


@register.simple_tag
def shared_url():
    return getattr(settings, "SHARED_URL", "/static")
