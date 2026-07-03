from django import template

from apis_core.uris.models import Uri

register = template.Library()


@register.simple_tag
def instance_uris(instance):
    """
    Return all URIs that point to a specific model instance
    """
    return Uri.objects.get_for_instance(instance)
