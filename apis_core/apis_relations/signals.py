from apis_core.apis_relations.models import TempTriple
from apis_core.apis_metainfo.models import RootObject
from apis_core.apis_metainfo.signals import post_duplicate
from django.dispatch import receiver

import logging

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
