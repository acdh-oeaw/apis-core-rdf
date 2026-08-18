from django.contrib.contenttypes.models import ContentType
from django.core.management.base import BaseCommand

from apis_core.search.models import SearchEntry
from apis_core.search.utils import get_models_registered_for_search


class Command(BaseCommand):
    help = "(Re)Index search entries"

    def add_arguments(self, parser):
        parser.add_argument(
            "--content-types",
            nargs="+",
            type=str,
            help='Specify the content types to reindex (e.g., "apis_ontology.model").',
        )
        parser.add_argument(
            "--recreate", action="store_true", help="Recreate existing search entries."
        )

    def handle(self, *args, **options):
        content_types = options.get("content_types") or []
        models = get_models_registered_for_search()

        if content_types:
            content_types = [ct.split(".") for ct in content_types]
            content_types = [
                ContentType.objects.get_by_natural_key(*ct) for ct in content_types
            ]
            content_types = [ct.model_class() for ct in content_types]
            models = set(models) & set(content_types)

            not_configured = set(content_types) - set(models)
            if not_configured:
                self.stdout.write(
                    "Models are not configured for search: "
                    + ", ".join(map(str, not_configured))
                )
            models = set(models) & set(content_types)

        for model in models:
            existing = []
            if not options.get("recreate"):
                existing = SearchEntry.objects.filter(
                    content_type=ContentType.objects.get_for_model(model)
                ).values("object_id")
            instances = model.objects.exclude(pk__in=existing)
            cnt = 1
            number_of_instances = instances.count()
            for instance in model.objects.exclude(pk__in=existing):
                self.stdout.write(
                    f"\rIndexing {cnt} of {number_of_instances} {model}", ending=""
                )
                self.stdout.flush()
                SearchEntry.reindex_model_instance(instance)
                cnt += 1
