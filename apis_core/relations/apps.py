from django.apps import AppConfig


class ApisRelations2Config(AppConfig):
    default_auto_field = "django.db.models.AutoField"
    name = "apis_core.relations"

    def ready(self):
        from . import signals
