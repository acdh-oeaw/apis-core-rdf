from django.apps import AppConfig


class RelationsConfig(AppConfig):
    default_auto_field = "django.db.models.AutoField"
    name = "apis_core.apis_relations"

    def ready(self):
        from . import signals  # noqa: F401
