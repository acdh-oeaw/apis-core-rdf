import logging

from django.contrib.contenttypes.models import ContentType
from django.db.models.signals import post_delete, post_save
from django.dispatch import receiver

from apis_core.generic.signals import post_duplicate, post_merge_with
from apis_core.relations.models import Relation
from apis_core.uris.utils import create_object_from_uri

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


@receiver(post_delete)
def set_relations_null(sender, instance, using, origin, **kwargs):
    content_type = ContentType.objects.get_for_model(instance)
    object_id = instance.pk
    if isinstance(object_id, int):
        Relation.objects.filter(
            subj_content_type=content_type, subj_object_id=object_id
        ).update(subj_object_id=None)
        Relation.objects.filter(
            obj_content_type=content_type, obj_object_id=object_id
        ).update(obj_object_id=None)


@receiver(post_save)
def create_relations(sender, instance, created, raw, using, update_fields, **kwargs):
    """
    This signal looks at the `create_relations_to_uris` attribute of a model
    instance. The attribute should contain a dict mapping between a relation
    name and mapping between they key `obj` or `subj` and a list of URIs.
    The signal then tries to create relations between the instance and the
    subjects or objects listed in the relation dict mapping.
    An example for the dict mapping would be:
    "myapp.livesin" = {
        curies = ["https://example.org/123"],
        obj = "apis_ontology.place"
    }
    """

    # disable the handler during fixture loading
    if raw:
        return
    relations = getattr(instance, "create_relations_to_uris", {})
    for relation, details in relations.items():
        relation_model = ContentType.objects.get_by_natural_key(
            *relation.split(".")
        ).model_class()

        target = details.get("obj", None) or details.get("subj", None)
        target_content_type = ContentType.objects.get_by_natural_key(*target.split("."))
        related_model = target_content_type.model_class()

        for related_uri in details["curies"]:
            try:
                related_instance = create_object_from_uri(
                    uri=related_uri, model=related_model
                )
                if details.get("obj"):
                    relation_model.object.create_between_instances(
                        instance, related_instance
                    )
                else:
                    relation_model.object.create_between_instances(
                        related_instance, instance
                    )
            except Exception as e:
                logger.error(
                    "Could not create relation to %s due to %s", related_uri, e
                )
