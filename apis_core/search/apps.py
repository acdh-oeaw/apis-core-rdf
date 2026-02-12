from django.apps import AppConfig


class SearchConfig(AppConfig):
    default_auto_field = "django.db.models.AutoField"
    name = "apis_core.search"

    def ready(self):
        from . import signals  # noqa: F401
