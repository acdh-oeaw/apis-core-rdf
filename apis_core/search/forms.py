from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit
from django import forms
from django.contrib.contenttypes.models import ContentType
from django.utils.translation import gettext_lazy as _

from apis_core.generic.templatetags.generic import get_genericmodels

from .models import SearchEntry


class ContentTypeMultipleChoiceField(forms.ModelMultipleChoiceField):
    def label_from_instance(self, obj):
        return obj.model_class().get_verbose_name_plural()


content_type_ids = SearchEntry.objects.values_list("content_type", flat=True).distinct()


def get_initial_content_types():
    models = [
        model
        for model in get_genericmodels()
        if getattr(model.Config, "search_initial", False)
    ]
    return [ContentType.objects.get_for_model(model) for model in models]


class SearchForm(forms.Form):
    query_str = forms.CharField(label=False)
    content_types = ContentTypeMultipleChoiceField(
        queryset=ContentType.objects.filter(id__in=content_type_ids),
        required=False,
        initial=get_initial_content_types(),
    )
    with_content = forms.BooleanField(required=False)

    query_str.widget.attrs.update({"placeholder": _("Search...")})

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_method = "GET"
        self.helper.add_input(Submit("submit", _("Submit")))
