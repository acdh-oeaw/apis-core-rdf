from apis_ontology.models import construct_properties
from django.core.management.base import BaseCommand, CommandError

from apis_core.apis_relations.models import Property


class Command(BaseCommand):
    help = (
        "Create and label relationships between entities by running "
        "the construct_properties() function in your app's models.py file."
    )

    def handle(self, *args, **options):
        try:
            construct_properties()
            self.stdout.write(
                self.style.SUCCESS("Successfully ran construct_properties()")
            )
        except Exception as e:
            raise CommandError(
                f"construct_properties() raised the " f"following error(s):\n{e}"
            )

        try:
            props = Property.objects.all()
        except Property.DoesNotExist:
            raise CommandError("No entity relationships exist.")

        if len(props) > 0:
            # TODO would ideally verify existence/validity of relevant fields
            #  as relationship names alone are useless w/o subj/obj references;
            #  below msg. purposefully only mentions "labels".
            self.stdout.write("The following labels now exist:")
            for p in props:
                self.stdout.write(self.style.SUCCESS(f"{p.name_forward}"), ending="")
                self.stdout.write(f" ... {p.name_reverse}")
        else:
            # construct_properties() starts out by deleting all existing
            # Property objects
            self.stdout.write(
                self.style.ERROR("No entity relationships found nor created.")
            )
