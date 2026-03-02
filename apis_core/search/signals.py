from django.contrib.contenttypes.models import ContentType
from django.core.serializers import serialize
from django.core.serializers.json import DjangoJSONEncoder
from django.db.models.signals import post_save
from django.dispatch import receiver

from .models import SearchEntry
from .registry import registry


@receiver(post_save, dispatch_uid="create_search_entry")
def create_default_uri(sender, instance, created, raw, using, update_fields, **kwargs):
    if raw:
        return
    if registry.is_registered(instance.__class__):
        content_type = ContentType.objects.get_for_model(instance)
        defaults = {
            "title": str(instance),
            "content": serialize("json", [instance], cls=DjangoJSONEncoder),
        }
        s, c = SearchEntry.objects.update_or_create(
            content_type=content_type, object_id=instance.pk, defaults=defaults
        )
