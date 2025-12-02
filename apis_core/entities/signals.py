import logging

from django.conf import settings
from django.contrib.contenttypes.models import ContentType
from django.db.models.signals import post_save
from django.dispatch import receiver

from apis_core.entities.abc import Entity
from apis_core.entities.models import EntityID
from apis_core.generic.signals import post_merge_with

logger = logging.getLogger(__name__)


@receiver(post_save)
def create_default_entity_id(
    sender, instance, created, raw, using, update_fields, **kwargs
):
    # disable the handler during fixture loading
    if raw:
        return

    if not isinstance(instance, Entity):
        return

    skip_entity_id_creation = getattr(instance, "skip_entity_id_creation", False)
    create_entity_ids = getattr(settings, "CREATE_ENTITY_IDS", True)
    if created and create_entity_ids and not skip_entity_id_creation:
        e = EntityID(content_object=instance)
        e.save()
        logger.info(
            "Created EntityID %s as a result of saving %s", repr(e), repr(instance)
        )


@receiver(post_merge_with)
def merge_entity_ids(sender, instance, entities, *args, **kwargs):
    for entity in entities:
        content_type = ContentType.objects.get_for_model(entity)
        for e in EntityID.objects.filter(
            content_type=content_type, object_id=entity.id
        ):
            logger.info(
                "Updating EntityID %s to point to %s as a result of merging %s",
                repr(e),
                repr(instance),
                repr(entity),
            )
            e.content_object = instance
            e.save()
