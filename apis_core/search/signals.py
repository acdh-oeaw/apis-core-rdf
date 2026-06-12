import logging

from django.db.models.signals import m2m_changed, post_delete, post_save
from django.dispatch import receiver

from apis_core.search.models import SearchEntry

from .registry import search

logger = logging.getLogger(__name__)


@receiver(post_save)
def create_or_update_search_entry(
    sender, instance, created, raw, using, update_fields, **kwargs
):
    if raw:
        return
    if search.is_registered(instance.__class__):
        logger.debug("Updating SearchEntry for %s", repr(instance))
        SearchEntry.reindex_model_instance(instance)

    # Update all related models on direct m2m changes
    for field in instance._meta.many_to_many:
        related_manager = getattr(instance, field.name)
        if search.is_registered(related_manager.model):
            for inst in related_manager.all():
                logger.debug("Updating SearchEntry for %s", repr(inst))
                SearchEntry.reindex_model_instance(inst)

    # Update related model instances on reverse m2m change
    # i.e. if an instance of Profession gets changed, update all
    # the Person instances that have that have
    # profession = ManyToManyField(Profession)
    for field in instance._meta.get_fields():
        if field.is_relation and field.many_to_many and field.auto_created:
            reverse_manager_name = getattr(field, "related_name") or f"{field.name}_set"
            reverse_manager = getattr(instance, reverse_manager_name)
            if search.is_registered(reverse_manager.model):
                options = search.get_options(reverse_manager.model)
                if reverse_manager.source_field_name in options.get(
                    "m2m_fields", set()
                ):
                    for inst in reverse_manager.all():
                        logger.debug("Updating SearchEntry for %s", repr(inst))
                        SearchEntry.reindex_model_instance(inst)


@receiver(m2m_changed)
def m2m_create_or_update_search_entry(
    sender, instance, action, reverse, model, pk_set, using, **kwargs
):
    if search.is_registered(instance.__class__):
        SearchEntry.reindex_model_instance(instance)


@receiver(post_delete)
def delete_search_entry(sender, instance, using, origin, **kwargs):
    if search.is_registered(instance.__class__):
        SearchEntry.delete(instance)
