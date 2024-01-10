from django import template
from django.contrib.contenttypes.models import ContentType

from apis_core.profile.models import Bookmark


register = template.Library()


@register.inclusion_tag("toggle_bookmark.html", takes_context=True)
def toggle_bookmark(context, model):
    content_type = ContentType.objects.get_for_model(model)
    context["content_type_id"] = content_type.id
    context["object_id"] = model.id
    context["exists"] = Bookmark.objects.filter(object_id=model.id, content_type=content_type, user=context.request.user.id).exists()
    return context
