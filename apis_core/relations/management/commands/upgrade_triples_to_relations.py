import os
from django.core.management.base import BaseCommand
from django.db.models.query import QuerySet
from django.conf import settings

from apis_core.apis_relations.models import Property


def to_camel_case(value):
    content = "".join(value.title().split())
    return content[0].lower() + content[1:]


def format_classes(value):
    if isinstance(value, QuerySet):
        if value.count() == 1:
            return value.first().model_class().__name__
        return "[" + ", ".join([format_classes(v) for v in value]) + "]"
    else:
        return value.model_class().__name__


template = """
class {relation_class}(Relation{additional_base_classes}):
    \"\"\"automatically generated class from property with id {prop_id}\"\"\"
    
    subj_model = {subj_model}
    obj_model = {obj_model}

    review = models.BooleanField(
        default=False,
        help_text="Should be set to True, if the data record holds up quality standards.",
    )
    start_date = models.DateField(blank=True, null=True)
    start_start_date = models.DateField(blank=True, null=True)
    start_end_date = models.DateField(blank=True, null=True)
    end_date = models.DateField(blank=True, null=True)
    end_start_date = models.DateField(blank=True, null=True)
    end_end_date = models.DateField(blank=True, null=True)
    start_date_written = models.CharField(
        max_length=255,
        blank=True,
        null=True,
        verbose_name="Start",
    )
    end_date_written = models.CharField(
        max_length=255,
        blank=True,
        null=True,
        verbose_name="End",
    )
    status = models.CharField(max_length=100)
    references = models.TextField(blank=True, null=True)
    notes = models.TextField(blank=True, null=True)

    @classmethod
    def name(self) -> str:
        return "{relation_label}"

    @classmethod
    def reverse_name(self) -> str:
        return "{reverse_relation_label}"
"""


class Command(BaseCommand):
    help = "Run through existing relations and create ng relation classes from the properties."

    def add_arguments(self, parser):
        parser.add_argument(
            "--file", type=str, help="File to write the new relation classes to."
        )
        parser.add_argument(
            "--auto_format",
            action="store_true",
            help="Whether to auto format the file using ruff (dependency needs to be available).",
        )

    def handle(self, *args, **options):
        classes = []
        for prop in Property.objects.all():
            classes.append(
                template.format(
                    relation_class=to_camel_case(prop.name_forward),
                    additional_base_classes=", VersionMixin"
                    if "apis_core.history" in settings.INSTALLED_APPS
                    else "",
                    prop_id=prop.id,
                    subj_model=format_classes(prop.subj_class.all()),
                    obj_model=format_classes(prop.obj_class.all()),
                    relation_label=prop.name_forward,
                    reverse_relation_label=prop.name_reverse,
                )
            )
        if options["file"]:
            with open(options["file"], "r") as of:
                with open(options["file"] + ".tmp", "w") as f:
                    f.write("from apis_core.relations.models import Relation\n")
                    f.write(of.read())
                    f.write(
                        "\n################################################\n#auto generated relation classes from properties\n################################################\n"
                    )
                    f.write("\n\n".join(classes))
                    f.seek(0)
            os.remove(options["file"])
            os.rename(options["file"] + ".tmp", options["file"])
            if options["auto_format"]:
                try:
                    import ruff

                    ruff.format_file(options["file"])
                    ruff.isort_file(options["file"])
                except ImportError:
                    print(
                        "Auto formatting not possible, ruff not available. Please install ruff."
                    )
