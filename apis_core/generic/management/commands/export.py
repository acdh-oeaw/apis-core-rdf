from pathlib import Path

from django.apps import apps
from django.contrib.contenttypes.models import ContentType
from django.core import serializers
from django.core.management.base import BaseCommand
from rest_framework.relations import RelatedField
from rest_framework.renderers import JSONRenderer

from apis_core.generic.abc import GenericModel
from apis_core.generic.helpers import first_member_match, module_paths
from apis_core.generic.renderers import CidocTTLRenderer
from apis_core.generic.serializers import (
    GenericHyperlinkedModelSerializer,
    serializer_factory,
)


class NaturalKeyRelatedField(RelatedField):
    def to_representation(self, value):
        content_type = ContentType.objects.get_for_model(value)
        return {
            "model": f"{content_type.app_label}.{content_type.model}",
            "pk": value.pk,
        }


class Command(BaseCommand):
    help = "Export data"

    def add_arguments(self, parser):
        parser.add_argument("path", type=Path)
        parser.add_argument(
            "--serializers",
            nargs="+",
            type=str,
            choices=["json", "jsonl", "drf_json", "drf_jsonl", "drf_cidoc_ttl"],
            default=["json"],
        )

    def get_serializer_class(self, model, prefix=""):
        serializer_class_modules = module_paths(
            model, path="serializers", suffix=f"{prefix}Serializer"
        )
        serializer_class = first_member_match(
            serializer_class_modules, GenericHyperlinkedModelSerializer
        )
        # We force the found serializer to use our NaturalKeyRelatedField
        # instead of the HyperlinkedRelatedField, which gives us a URI
        serializer_class.serializer_related_field = NaturalKeyRelatedField
        # We fore the url_field name to be `id`, which is a hack - the
        # HyperlinkedModelSerializer seems to replace the "id" with a URI,
        # but if we set the `uri_field_name` to `id` it gets overwritten
        # wit the original value again.
        serializer_class.url_field_name = "id"
        return serializer_factory(model, serializer=serializer_class)

    def serialize_json(self, model, content_type_str):
        folder = self.output / "json" / content_type_str
        folder.mkdir(parents=True, exist_ok=True)
        serializer = serializers.get_serializer("json")
        for instance in model.objects.all():
            data = serializer().serialize(
                [
                    instance,
                ],
                indent=2,
                use_natural_foreign_keys=True,
                use_natural_primary_keys=True,
            )
            file = folder / f"{instance.pk:06}.json"
            file.write_text(data)

    def serialize_jsonl(self, model, content_type_str):
        folder = self.output / "jsonl"
        folder.mkdir(parents=True, exist_ok=True)

        serializer = serializers.get_serializer("jsonl")
        data = serializer().serialize(
            model.objects.all(),
            indent=2,
            use_natural_foreign_keys=True,
            use_natural_primary_keys=True,
        )
        file = folder / f"{content_type_str}.jsonl"
        file.write_text(data)

    def serialize_drf_json(self, model, content_type_str):
        folder = self.output / "drf_json" / content_type_str
        folder.mkdir(parents=True, exist_ok=True)

        Serializer = self.get_serializer_class(model)

        for instance in model.objects.all():
            data = Serializer(instance, context={"request": None}).data
            file = folder / f"{instance.pk:06}.json"
            file.write_text(
                JSONRenderer()
                .render(data, accepted_media_type="application/json; indent=2")
                .decode()
            )

    def serialize_drf_jsonl(self, model, content_type_str):
        folder = self.output / "drf_jsonl"
        folder.mkdir(parents=True, exist_ok=True)

        Serializer = self.get_serializer_class(model)

        lines = []
        for instance in model.objects.all():
            data = Serializer(instance, context={"request": None}).data
            lines.append(JSONRenderer().render(data).decode())
        file = folder / f"{content_type_str}.jsonl"
        file.write_text("\n".join(lines))

    def serialize_drf_cidoc_ttl(self, model, content_type_str):
        folder = self.output / "drf_rdf"
        folder.mkdir(parents=True, exist_ok=True)

        Serializer = self.get_serializer_class(model, prefix="Cidoc")

        data = {
            "results": Serializer(
                model.objects.all(), context={"request": None}, many=True
            ).data
        }
        file = folder / f"{content_type_str}.cidoc.ttl"
        file.write_text(CidocTTLRenderer().render(data))

    def handle(self, *args, **options):
        self.output = options["path"]
        self.output.mkdir(parents=True, exist_ok=True)

        for model in apps.get_models():
            if issubclass(model, GenericModel):
                content_type = ContentType.objects.get_for_model(model)
                content_type_str = f"{content_type.app_label}.{content_type.model}"
                print(
                    f"Serializing {model} instances (content type: {content_type_str})"
                )

                for serializer in options["serializers"]:
                    getattr(self, f"serialize_{serializer}")(model, content_type_str)
