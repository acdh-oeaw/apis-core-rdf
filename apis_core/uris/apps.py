from django.apps import AppConfig


class MetainfoConfig(AppConfig):
    default_auto_field = "django.db.models.AutoField"
    name = "apis_core.uris"

    def ready(self):
        from . import signals  # noqa: F401
