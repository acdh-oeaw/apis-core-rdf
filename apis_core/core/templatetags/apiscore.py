from django import template
from django.conf import settings
from django.contrib.contenttypes.models import ContentType


register = template.Library()


@register.simple_tag
def shared_url():
    return getattr(settings, "SHARED_URL", "/static/")


@register.simple_tag
def page_range(paginator, number):
    return paginator.get_elided_page_range(number=number)


@register.filter
def contenttype(model):
    return ContentType.objects.get_for_model(model)


@register.filter
def count(model):
    return model.__class__.objects.count()
