from django.contrib.contenttypes.models import ContentType
from django.core.management.base import BaseCommand

from apis_core.search.models import SearchEntry
from apis_core.search.registry import search


class Command(BaseCommand):
    help = "(Re)Index search entries"

    def add_arguments(self, parser):
        parser.add_argument(
            "--content-types",
            nargs="+",
            type=str,
            help='Specify the content types to reindex (e.g., "apis_ontology.model").',
        )

    def handle(self, *args, **options):
        content_types = options.get("content_types") or []
        registered_models = search.get_registered_models()

        if not registered_models:
            self.stdout.write(
                "No models are registerd for search. Add the @search.register decorator to the models that should be searchable"
            )

        if content_types:
            content_types = [ct.split(".") for ct in content_types]
            content_types = [
                ContentType.objects.get_by_natural_key(*ct) for ct in content_types
            ]
            content_types = [ct.model_class() for ct in content_types]

            not_registered = set(content_types) - set(registered_models)
            if not_registered:
                self.stdout.write(
                    "Models are not registered: " + ", ".join(map(str, not_registered))
                )
            registered_models = set(registered_models) & set(content_types)

        for model in registered_models:
            self.stdout.write(f"Indexing all in {model}")
            for instance in model.objects.all():
                SearchEntry.reindex_model_instance(instance)
