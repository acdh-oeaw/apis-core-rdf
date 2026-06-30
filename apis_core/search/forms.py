from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit
from django import forms
from django.contrib.contenttypes.models import ContentType
from django.utils.translation import gettext_lazy as _

from apis_core.search.registry import search


def get_models():
    return {
        ContentType.objects.get_for_model(i).id: i.get_verbose_name_plural()
        for i in search.get_registered_models()
    }


class SearchForm(forms.Form):
    query_str = forms.CharField()
    content_types = forms.MultipleChoiceField(choices=get_models(), required=False)
    with_content = forms.BooleanField(required=False)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_method = "GET"
        self.helper.add_input(Submit("submit", _("Submit")))
