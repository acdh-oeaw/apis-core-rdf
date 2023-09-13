from django.core.management.base import BaseCommand
from apis_core.apis_relations.models import TempTriple


class Command(BaseCommand):
    help = "Create relations based on all existing TempTriples"

    def handle(self, *args, **options):
        for tt in TempTriple.objects.all():
            tt.save()
