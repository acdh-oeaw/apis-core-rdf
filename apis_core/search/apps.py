from django.apps import AppConfig
from django.db.models.signals import m2m_changed, post_delete, post_save

from .registry import search


class SearchConfig(AppConfig):
    default_auto_field = "django.db.models.AutoField"
    name = "apis_core.search"

    def ready(self):
        from .signals import (
            create_or_update_search_entry,
            delete_search_entry,
            m2m_create_or_update_search_entry,
        )

        for model in search.get_registered_models():
            post_save.connect(create_or_update_search_entry, model)
            m2m_changed.connect(m2m_create_or_update_search_entry, model)
            post_delete.connect(delete_search_entry, model)
