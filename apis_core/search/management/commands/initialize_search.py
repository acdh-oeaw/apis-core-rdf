from django.core.management.base import BaseCommand

from apis_core.search.registry import registry
from apis_core.search.utils import reindex_model_instance


class Command(BaseCommand):
    help = "(Re)Index search entries"

    def handle(self, *args, **options):
        for model in registry.get_registered_models():
            for instance in model.objects.all():
                reindex_model_instance(instance)
