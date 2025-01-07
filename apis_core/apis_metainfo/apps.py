import logging

from django.apps import AppConfig
from django.conf import settings

logger = logging.getLogger(__name__)


class MetainfoConfig(AppConfig):
    default_auto_field = "django.db.models.AutoField"
    name = "apis_core.apis_metainfo"

    def ready(self):
        from . import signals  # noqa: F401

        if getattr(settings, "APIS_BASE_URI", None) is None:
            logger.warning(
                "You should set the APIS_BASE_URI setting - we are using https://example.org as a fallback!"
            )
