from django.forms import ModelChoiceField
from django.core.exceptions import ValidationError
from apis_core.generic.helpers import first_match_via_mro
from apis_core.apis_metainfo.models import Uri


class ModelImportChoiceField(ModelChoiceField):
    def to_python(self, value):
        if value.startswith("http"):
            try:
                uri = Uri.objects.get(uri=value)
                return uri.root_object
            except Uri.DoesNotExist:
                Importer = first_match_via_mro(
                    self.queryset.model,
                    path="importers",
                    suffix="Importer",
                )
                if Importer is not None:
                    importer = Importer(value, self.queryset.model)
                    instance = importer.create_instance()
                    uri = Uri.objects.create(uri=importer.get_uri, root_object=instance)
                    return instance
                raise ValidationError(
                    "Could not find an importer for: %(url)s", params={"url": value}
                )
        return super().to_python(value)
