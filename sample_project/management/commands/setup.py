import pathlib
import secrets
from datetime import datetime

from django.contrib.auth.models import User
from django.core.management.base import BaseCommand


class Command(BaseCommand):
    help = "Set up APIS test instance"

    def handle(self, *app_labels, **options):
        password = secrets.token_urlsafe(8)
        User.objects.create_superuser(
            username="admin", email="admin@example.org", password=password
        )
        pathlib.Path("/tmp/password.txt").write_text(password)
        pathlib.Path("/tmp/startup.txt").write_text(str(datetime.utcnow()))
