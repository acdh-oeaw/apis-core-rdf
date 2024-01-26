from django.apps import AppConfig


class LoggingConfig(AppConfig):
    default_auto_field = "django.db.models.AutoField"
    name = "apis_core.logging"

    def ready(self):
        from . import signals
