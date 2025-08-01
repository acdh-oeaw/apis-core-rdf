from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit
from django import forms
from django.utils.translation import gettext_lazy as _

from apis_core.collections.models import SkosCollection


class CollectionObjectForm(forms.Form):
    collections = forms.ModelMultipleChoiceField(
        required=False, queryset=SkosCollection.objects.all(), label=_("Collections")
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.add_input(Submit("submit", _("Submit")))
