import logging

from django.dispatch import receiver

from apis_core.apis_metainfo.models import RootObject
from apis_core.apis_relations.models import TempTriple
from apis_core.generic.signals import post_duplicate, post_merge_with

logger = logging.getLogger(__name__)


@receiver(post_duplicate)
def copy_relations(sender, instance, duplicate, **kwargs):
    logger.info(f"Copying relations from {instance} to {duplicate}")
    if isinstance(instance, RootObject):
        for rel in TempTriple.objects.filter(subj=instance):
            newrel = rel.duplicate()
            newrel.subj = duplicate
            newrel.save()
        for rel in TempTriple.objects.filter(obj=instance):
            newrel = rel.duplicate()
            newrel.obj = duplicate
            newrel.save()


@receiver(post_merge_with)
def merge_relations(sender, instance, entities, **kwargs):
    for ent in entities:
        logger.info(f"Merging relations from {ent!r} into {instance!r}")
        TempTriple.objects.filter(obj__id=ent.id).update(obj=instance)
        TempTriple.objects.filter(subj__id=ent.id).update(subj=instance)
