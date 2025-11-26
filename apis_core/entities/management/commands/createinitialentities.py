from django.apps import apps
from django.contrib.contenttypes.models import ContentType
from django.core.management.base import BaseCommand

from apis_core.entities.models import Entity, EntityID


class Command(BaseCommand):
    help = "Create entities for all entities"

    def handle(self, *args, **options):
        for model in apps.get_models():
            if issubclass(model, Entity):
                content_type = ContentType.objects.get_for_model(model)
                counter = 0
                for entity in model.objects.all():
                    entity, created = EntityID.objects.get_or_create(
                        pk=entity.pk, content_type=content_type, object_id=entity.pk
                    )
                    if created:
                        counter += 1
                print(f"Created EntityIDs for {counter} entities of type {model}")
