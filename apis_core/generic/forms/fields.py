from django.core.exceptions import ValidationError
from django.forms import ModelChoiceField
from django.utils.translation import gettext as _

from apis_core.utils.helpers import create_object_from_uri


class ModelImportChoiceField(ModelChoiceField):
    def to_python(self, value):
        result = None
        try:
            result = create_object_from_uri(value, self.queryset.model)
        except Exception as e:
            raise ValidationError(
                _("Could not import %(value)s: %(exception)s"),
                params={"value": value, "exception": e},
            )
        return result or super().to_python(value)
