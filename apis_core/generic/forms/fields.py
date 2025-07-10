from django.core.exceptions import ValidationError
from django.forms import ModelChoiceField, MultiValueField, MultiWidget
from django.utils.translation import gettext as _

from apis_core.apis_metainfo.utils import create_object_from_uri


class ModelImportChoiceField(ModelChoiceField):
    def to_python(self, value):
        result = None
        if value.startswith(("http://", "https://")):
            try:
                result = create_object_from_uri(
                    value, self.queryset.model, raise_on_fail=True
                )
            except Exception as e:
                raise ValidationError(
                    _("Could not import %(value)s: %(exception)s"),
                    params={"value": value, "exception": e},
                )
        return result or super().to_python(value)


class RowColumnMultiWidget(MultiWidget):
    """
    A custom MultiWidget that is meant to be used with the
    RowColumnMultiValueField. The widget takes a list of widgets
    as a parameter and displays those widgets in columns in one row.
    The `labels` parameter is used to add a separate label to the
    individual widgets.
    """

    template_name = "widgets/row_column_multiwidget.html"
    use_fieldset = False

    def __init__(self, widgets, labels=[], attrs=None):
        self.labels = labels
        super().__init__(widgets, attrs)

    def get_context(self, name, value, attrs):
        ctx = super().get_context(name, value, attrs)
        for widget in ctx["widget"]["subwidgets"]:
            if self.labels:
                widget["label"] = self.labels.pop(0)
        return ctx

    def decompress(self, value):
        if value:
            return value
        return []


class RowColumnMultiValueField(MultiValueField):
    """
    This is a custom MultiValueField that simply shows multiple form
    fields in a row. The form fields are passed to the constructor and
    the corresponding RowColumnMultiWidget simply iterates through all
    the fields and shows them in rows.
    Additionaly it is possible to pass a list of `labels` that are then
    also passed on to the widget, which uses those to add a separate
    label to the individual widgets.
    """

    def __init__(self, fields, labels=[], *args, **kwargs):
        kwargs["widget"] = RowColumnMultiWidget(
            widgets=[f.widget for f in fields], labels=labels
        )
        super().__init__(fields, *args, **kwargs)

    def compress(self, data_list):
        return data_list
