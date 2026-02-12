import logging

from .models import SearchEntry

logger = logging.getLogger(__name__)


def create_or_update_search_entry(
    sender, instance, created, raw, using, update_fields, **kwargs
):
    """
    Update the SearchEntry entry for a model instance.
    This also updates model instances that are connected via a
    `ManyToManyField`.
    It also updates reverse related ManyToManyField if they are
    listed in the `m2m_fields` options of the search registry.
    """
    if raw or getattr(instance, "skip_searchentry_update", False):
        return
    logger.debug("Updating SearchEntry for %s", repr(instance))
    SearchEntry.reindex_model_instance(instance)

    # Update all related models on direct m2m changes
    for field in instance._meta.many_to_many:
        related_manager = getattr(instance, field.name)
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
            m2m_fields = getattr(reverse_manager.model.Config, "search_follow_m2m", [])
            if reverse_manager.source_field_name in m2m_fields:
                for inst in reverse_manager.all():
                    logger.debug("Updating SearchEntry for %s", repr(inst))
                    SearchEntry.reindex_model_instance(inst)


def m2m_create_or_update_search_entry(
    sender, instance, action, reverse, model, pk_set, using, **kwargs
):
    """
    Update all related ManyToManyField instances, if a ManyToManyField changes.
    This is primarily useful because the m2m fields are changed *after* a model
    instance is saved, so the `create_or_update_search_entry` above doesn't know
    about the changed m2m field yet. It is also useful if the m2m field is changed
    programmatically and the `save()` method isn't run at all.
    """
    if action in ("post_add", "post_remove", "post_clear"):
        for inst in model.objects.filter(pk__in=pk_set):
            logger.debug(
                "Updating SearchEntry for %s (m2m_create_or_update_search_entry)",
                repr(inst),
            )
        SearchEntry.reindex_model_instance(inst)


def delete_search_entry(sender, instance, using, origin, **kwargs):
    SearchEntry.delete_by_instance(instance)
