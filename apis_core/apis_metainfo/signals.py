import logging

from django.contrib.contenttypes.models import ContentType
from django.db.models.signals import post_delete
from django.dispatch import receiver

from apis_core.apis_metainfo.models import Uri

logger = logging.getLogger(__name__)


@receiver(post_delete)
def remove_stale_uris(sender, instance, *args, **kwargs):
    content_type = ContentType.objects.get_for_model(instance)
    if isinstance(instance.pk, int):
        uris = Uri.objects.filter(content_type=content_type, object_id=instance.pk)
        for uri in uris:
            logger.info(
                "Deleting uri %s as a result of deleting %s", repr(uri), repr(instance)
            )
            uri.delete()
