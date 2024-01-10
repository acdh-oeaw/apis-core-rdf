from django.core.management.base import BaseCommand
from django.db import transaction

from apis_core.apis_metainfo.models import Uri
from apis_core.utils.normalize import clean_uri


class Command(BaseCommand):
    # Show this when the user types help
    help = "normalizes Uris"

    def handle(self, *args, **options):
        with transaction.atomic():
            for x in Uri.objects.all():
                old_uri = x.uri
                new_uri = clean_uri(old_uri)
                if old_uri != new_uri:
                    x.uri = new_uri
                    x.save()
        return "all done"
