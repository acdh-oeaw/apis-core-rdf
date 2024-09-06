from crum import get_current_request
from django.contrib import messages
from django.contrib.contenttypes.models import ContentType
from django.db.models.signals import post_save
from django.dispatch import receiver

from apis_core.collections.models import SkosCollection, SkosCollectionContentObject
from apis_core.history.models import APISHistoryTableBase


@receiver(post_save)
def add_to_session_collection(
    sender, instance, created, raw, using, update_fields, **kwargs
):
    """
    Add a created apis_core.history model instance to all the SkosCollections
    that are listed in the `session_collections` session variable.
    This needs the 'crum.CurrentRequestUserMiddleware' middleware to
    be enabled.
    """
    request = get_current_request()
    if isinstance(instance, APISHistoryTableBase) and request:
        for pk in request.session.get("session_collections", []):
            sc = SkosCollection.objects.get(pk=pk)
            content_type = ContentType.objects.get_for_model(instance)
            SkosCollectionContentObject.objects.create(
                collection=sc,
                content_type=content_type,
                object_id=instance.history_id,
            )
            messages.info(request, f"Tagged {instance} with tag {sc}")
