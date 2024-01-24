from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit
from dal import autocomplete
from django import forms
from django.contrib.contenttypes.models import ContentType
from django.urls import reverse

from apis_core.generic.forms.fields import ModelImportChoiceField


class EntitiesMergeForm(forms.Form):
    def __init__(self, *args, **kwargs):
        if "instance" in kwargs:
            instance = kwargs.pop("instance")
        super().__init__(*args, **kwargs)
        ct = ContentType.objects.get_for_model(instance)
        self.fields["uri"] = ModelImportChoiceField(
            queryset=ct.model_class().objects.all()
        )
        uri = reverse("apis_core:generic:autocomplete", args=[ct])
        attrs = {"data-placeholder": "Search ...", "data-minimum-input-length": 3}
        self.fields["uri"].widget = autocomplete.ModelSelect2(uri, attrs=attrs)
        self.fields["uri"].widget.choices = self.fields["uri"].choices
        entitytype = instance._meta.verbose_name
        help_text = f"""The attributes of the source {entitytype} you
        choose will be copied/moved to this one and the source
        {entitytype} will then be deleted."""
        self.fields["uri"].help_text = help_text
        self.fields["uri"].label = "Merge with..."
        self.helper = FormHelper()
        self.helper.add_input(Submit("submit", "Submit"))
        self.helper.form_action = reverse(
            "apis_core:apis_entities:generic_entities_merge_view",
            args=[instance.__class__.__name__.lower(), instance.pk],
        )
