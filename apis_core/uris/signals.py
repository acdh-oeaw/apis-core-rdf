import logging

from django.conf import settings
from django.contrib.contenttypes.models import ContentType
from django.db.models.signals import post_delete, post_save
from django.dispatch import receiver

from apis_core.generic.signals import post_merge_with
from apis_core.uris.models import Uri

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


@receiver(post_save, dispatch_uid="create_default_uri")
def create_default_uri(sender, instance, created, raw, using, update_fields, **kwargs):
    # disable the handler during fixture loading
    if raw:
        return
    # The list of Uris that should be created
    uris = getattr(instance, "_uris", [])

    # If this is a new object (created) we ask the model for its
    # default Uri and add that to the list of Uris
    skip_default_uri = getattr(instance, "skip_default_uri", False)
    create_default_uri = getattr(settings, "CREATE_DEFAULT_URI", True)
    if created and create_default_uri and not skip_default_uri:
        try:
            uris.append(instance.get_default_uri())
        except AttributeError:
            pass

    # We first check if there are even any Uris to create before we
    # lookup the content_type. This is a bit of a workaround, because
    # during migration the signal is triggered, but the lookup would
    # fail.
    if uris:
        content_type = ContentType.objects.get_for_model(instance)
        for uri in uris:
            logger.info(
                "Creating uri %s as a result of saving %s", repr(uri), repr(instance)
            )
            Uri.objects.get_or_create(
                uri=uri, content_type=content_type, object_id=instance.id
            )


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
