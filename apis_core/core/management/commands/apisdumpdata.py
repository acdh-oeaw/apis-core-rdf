from django.core.management.base import BaseCommand

from apis_core.utils.helpers import datadump_serializer


class Command(BaseCommand):
    help = "Dump APIS data"

    def add_arguments(self, parser):
        parser.add_argument(
            "args",
            metavar="app_labels",
            nargs="*",
            help=("Optional additional app_labels."),
        )

    def handle(self, *app_labels, **options):
        print(datadump_serializer(app_labels, "json"))
