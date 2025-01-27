from django.core.exceptions import ValidationError
from django.forms import ChoiceField, ModelChoiceField, MultiValueField, MultiWidget
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


class IncludeExcludeMultiWidget(MultiWidget):
    template_name = "widgets/includeexclude_multiwidget.html"
    use_fieldset = False

    def decompress(self, value):
        return [value, value]


class IncludeExcludeField(MultiValueField):
    """
    This is a custom MultiValueField that adds a ChoiceField that only provides two
    choices, namely `exclude` and `include`. It can be used for django-filter filters
    to specify which action should be done with the filter.
    """

    def __init__(self, field, *args, **kwargs):
        fields = (
            field,
            ChoiceField(choices=[("include", "include"), ("exclude", "exclude")]),
        )
        kwargs["widget"] = IncludeExcludeMultiWidget(widgets=[f.widget for f in fields])
        super().__init__(fields=fields, *args, **kwargs)

    def compress(self, data_list):
        return data_list
