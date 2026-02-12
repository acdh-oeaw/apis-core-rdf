from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit
from django import forms
from django.contrib.contenttypes.models import ContentType
from django.utils.translation import gettext_lazy as _

from .models import SearchEntry


class ContentTypeMultipleChoiceField(forms.ModelMultipleChoiceField):
    def label_from_instance(self, obj):
        return obj.model_class().get_verbose_name_plural()


content_type_ids = SearchEntry.objects.values_list("content_type", flat=True).distinct()


class SearchForm(forms.Form):
    query_str = forms.CharField()
    content_types = ContentTypeMultipleChoiceField(
        queryset=ContentType.objects.filter(id__in=content_type_ids), required=False
    )
    with_content = forms.BooleanField(required=False)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_method = "GET"
        self.helper.add_input(Submit("submit", _("Submit")))
