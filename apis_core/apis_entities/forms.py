from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit
from dal import autocomplete
from django import forms
from django.contrib.contenttypes.models import ContentType
from django.urls import reverse


class EntitiesMergeForm(forms.Form):
    def __init__(self, *args, **kwargs):
        if "instance" in kwargs:
            instance = kwargs.pop("instance")
        super().__init__(*args, **kwargs)
        ct = ContentType.objects.get_for_model(instance)
        self.fields["uri"] = forms.ModelChoiceField(
            queryset=ct.model_class().objects.all()
        )
        uri = reverse("apis_core:generic:autocomplete", args=[ct])
        attrs = {
            "data-placeholder": "Search ...",
            "data-minimum-input-length": 3,
            "data-html": True,
        }
        self.fields["uri"].widget = autocomplete.ModelSelect2(uri, attrs=attrs)
        self.fields["uri"].widget.choices = self.fields["uri"].choices
        self.fields["uri"].label = "Merge with..."
        self.helper = FormHelper()
        self.helper.form_method = "GET"
        self.helper.add_input(Submit("submit", "Submit"))
        self.helper.form_action = instance.get_enrich_url()
