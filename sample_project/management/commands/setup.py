from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
import secrets


class Command(BaseCommand):
    help = "Set up APIS test instance"

    def handle(self, *app_labels, **options):
        password = secrets.token_urlsafe(8)
        print(f"Password for admin user is: {password}")
        User.objects.create_superuser(
            username="admin", email="admin@example.org", password=password
        )
