from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit
from django import forms
from django.core.exceptions import ValidationError
from apis_core.generic.forms import GenericModelForm

from .models import Uri


class UriForm(GenericModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper.form_class = "form-horizontal"
        self.helper.label_class = "col-md-3"
        self.helper.field_class = "col-md-9"


class UriGetOrCreateForm(forms.Form):
    uri = forms.URLField()

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.add_input(
            Submit("submit", "save"),
        )

    def clean_uri(self):
        self.uriobj, _ = Uri.objects.get_or_create(uri=self.cleaned_data["uri"])
        # This is a workaround until we decide to make the `root_object` ForeignKey
        # a required field
        if not self.uriobj.root_object:
            self.uriobj.delete()
            raise ValidationError("Could not create object from Uri")
