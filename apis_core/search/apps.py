from django.apps import AppConfig
from django.db.models.signals import m2m_changed, post_delete, post_save


class SearchConfig(AppConfig):
    default_auto_field = "django.db.models.AutoField"
    name = "apis_core.search"

    def ready(self):
        from .signals import (
            create_or_update_search_entry,
            delete_search_entry,
            m2m_create_or_update_search_entry,
        )
        from .utils import get_models_registered_for_search

        for model in get_models_registered_for_search():
            post_save.connect(create_or_update_search_entry, model)
            post_delete.connect(delete_search_entry, model)
            for m2m_field in getattr(model.Config, "search_follow_m2m", []):
                through_field = model._meta.get_field(m2m_field).remote_field.through
                m2m_changed.connect(m2m_create_or_update_search_entry, through_field)
