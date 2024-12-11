import logging

from django.contrib.contenttypes.models import ContentType
from django.dispatch import receiver

from apis_core.generic.signals import post_duplicate, post_merge_with
from apis_core.relations.models import Relation

logger = logging.getLogger(__name__)


@receiver(post_duplicate)
def copy_relations(sender, instance, duplicate, **kwargs):
    logger.info(f"Copying relations from {instance!r} to {duplicate!r}")
    content_type = ContentType.objects.get_for_model(instance)
    subj_rels = Relation.objects.filter(
        subj_content_type=content_type, subj_object_id=instance.id
    ).select_subclasses()
    obj_rels = Relation.objects.filter(
        obj_content_type=content_type, obj_object_id=instance.id
    ).select_subclasses()
    for rel in subj_rels:
        rel.pk = None
        rel.id = None
        rel.subj_object_id = duplicate.id
        rel.save()
    for rel in obj_rels:
        rel.pk = None
        rel.id = None
        rel.obj_object_id = duplicate.id
        rel.save()


@receiver(post_merge_with)
def merge_relations(sender, instance, entities, **kwargs):
    for ent in entities:
        logger.info(f"Merging relations from {ent!r} into {instance!r}")
        content_type = ContentType.objects.get_for_model(ent)
        Relation.objects.filter(
            subj_content_type=content_type, subj_object_id=ent.id
        ).update(subj_object_id=instance.id)
        Relation.objects.filter(
            obj_content_type=content_type, obj_object_id=ent.id
        ).update(obj_object_id=instance.id)
