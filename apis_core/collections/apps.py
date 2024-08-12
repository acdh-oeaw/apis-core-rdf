from django.apps import AppConfig


class VocabsConfig(AppConfig):
    default_auto_field = "django.db.models.AutoField"
    name = "apis_core.collections"

    def ready(self):
        from . import signals  # noqa: F401
