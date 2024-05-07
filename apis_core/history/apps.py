from django.apps import AppConfig


class HistoryConfig(AppConfig):
    name = "apis_core.history"

    def ready(self):
        from . import signals  # noqa: F401
