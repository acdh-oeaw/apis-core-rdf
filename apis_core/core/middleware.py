import logging
from pathlib import Path

from django.conf import settings
from django.shortcuts import render

logger = logging.getLogger(__name__)


class MaintenanceMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        maintenance_file = getattr(
            settings, "APIS_MAINTENANCE_FILE", "apis_maintenance"
        )
        if Path(maintenance_file).exists():
            logger.warning("Site is running in maintenance mode")
            if hasattr(request, "user"):
                if request.user.is_superuser:
                    return self.get_response(request)
            return render(request, "maintenance.html")
        return self.get_response(request)
