from django import forms
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _

from apis_core.generic.forms import GenericModelForm

from .models import Uri


class UriForm(GenericModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper.form_class = "form-horizontal"
        self.helper.label_class = "col-md-3"
        self.helper.field_class = "col-md-9"


def validate_uri(value):
    if Uri.objects.filter(uri=value).exists():
        uri = Uri.objects.get(uri=value)
        raise ValidationError(
            _("%(value)s already exists on %(object)s"),
            params={"value": value, "object": uri.content_object},
        )


class UriCreateFromObjectForm(forms.Form):
    uri = forms.URLField(validators=[validate_uri])
