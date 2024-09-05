from django import template
from django.conf import settings
from apis_core import __version__
from django.urls import reverse


register = template.Library()


@register.simple_tag
def shared_url():
    return getattr(settings, "SHARED_URL", "/static/")


@register.simple_tag
def page_range(paginator, number):
    return paginator.get_elided_page_range(number=number)


@register.filter
def opts(obj):
    return obj._meta


@register.filter
def model_meta(content_type, field):
    return getattr(content_type.model_class()._meta, field)


@register.simple_tag
def apis_version():
    return __version__


@register.inclusion_tag("partials/api.html")
def api():
    return {"api_root": reverse("apis_core:apis_api:api-root")}
