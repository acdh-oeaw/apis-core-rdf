from django.apps import AppConfig


class EntityConfig(AppConfig):
    default_auto_field = "django.db.models.AutoField"
    name = "apis_core.entities"

    def ready(self):
        from . import signals  # noqa: F401
