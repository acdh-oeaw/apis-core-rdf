from django.db.models.signals import post_save
from django.dispatch import receiver

from .registry import registry
from .utils import reindex_model_instance


@receiver(post_save, dispatch_uid="create_search_entry")
def create_default_uri(sender, instance, created, raw, using, update_fields, **kwargs):
    if raw:
        return
    if registry.is_registered(instance.__class__):
        reindex_model_instance(instance)
