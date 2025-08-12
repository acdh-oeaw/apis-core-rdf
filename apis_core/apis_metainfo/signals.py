import logging

from django.contrib.contenttypes.models import ContentType
from django.db.models.signals import post_delete
from django.dispatch import receiver

from apis_core.apis_metainfo.models import Uri
from apis_core.generic.signals import post_merge_with

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


@receiver(post_merge_with)
def merge_uris(sender, instance, entities, *args, **kwargs):
    instance_content_type = ContentType.objects.get_for_model(instance)
    for entity in entities:
        content_type = ContentType.objects.get_for_model(entity)
        for uri in Uri.objects.filter(content_type=content_type, object_id=entity.id):
            logger.info(
                "Updating uri %s to point to %s as a result of merging %s",
                repr(uri),
                repr(instance),
                repr(entity),
            )
            uri.content_type = instance_content_type
            uri.object_id = instance.id
            uri.save()
