from django.forms import ModelChoiceField
from apis_core.utils.helpers import create_object_from_uri


class ModelImportChoiceField(ModelChoiceField):
    def to_python(self, value):
        result = create_object_from_uri(value, self.queryset.model)
        if result is not None:
            return result
        return super().to_python(value)
