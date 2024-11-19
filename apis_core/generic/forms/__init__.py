from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit
from dal import autocomplete
from django import forms
from django.contrib.contenttypes.models import ContentType
from django.urls import reverse

from apis_core.generic.abc import GenericModel
from apis_core.generic.forms.fields import ModelImportChoiceField


class GenericImportForm(forms.Form):
    class Meta:
        fields = []

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["url"] = ModelImportChoiceField(
            queryset=self.Meta.model.objects.all()
        )
        ct = ContentType.objects.get_for_model(self.Meta.model)
        url = reverse("apis_core:generic:autocompleteexternalonly", args=[ct])
        self.fields["url"].widget = autocomplete.ModelSelect2(
            url, attrs={"data-html": True, "data-tags": 1}
        )
        self.fields["url"].widget.choices = self.fields["url"].choices
        self.helper = FormHelper()
        self.helper.add_input(Submit("submit", "Submit"))


class GenericFilterSetForm(forms.Form):
    """
    FilterSet form for generic models
    Adds a submit button using the django crispy form helper
    Adds a `columns` selector that lists all the fields from
    the model
    """

    columns_exclude = []

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.helper = FormHelper()
        self.helper.form_method = "GET"
        self.helper.add_input(Submit("submit", "Submit"))

    def clean(self):
        self.cleaned_data = super().clean()
        self.cleaned_data.pop("columns", None)
        return self.cleaned_data


class GenericModelForm(forms.ModelForm):
    """
    Model form for generic models
    Adds a submit button using the django crispy form helper
    and sets the ModelChoiceFields and ModelMultipleChoiceFields
    to use autocomplete replacement fields
    """

    class Meta:
        fields = "__all__"

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper(self)
        self.helper.add_input(Submit("submit", "Submit"))

        # override the fields pointing to other models,
        # to make them use the autocomplete widgets
        override_fieldtypes = {
            "ModelMultipleChoiceField": autocomplete.ModelSelect2Multiple,
            "ModelChoiceField": autocomplete.ModelSelect2,
            "ModelImportChoiceField": autocomplete.ModelSelect2,
        }
        for field in self.fields:
            clsname = self.fields[field].__class__.__name__
            if clsname in override_fieldtypes.keys():
                ct = ContentType.objects.get_for_model(
                    self.fields[field]._queryset.model
                )
                if issubclass(ct.model_class(), GenericModel):
                    url = reverse("apis_core:generic:autocomplete", args=[ct])
                    self.fields[field].widget = override_fieldtypes[clsname](
                        url, attrs={"data-html": True}
                    )
                    self.fields[field].widget.choices = self.fields[field].choices


class GenericMergeForm(forms.Form):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.add_input(Submit("submit", "Merge"))


class GenericEnrichForm(forms.Form):
    def __init__(self, *args, **kwargs):
        data = kwargs.pop("data", {})
        instance = kwargs.pop("instance", None)
        super().__init__(*args, **kwargs)
        for key, value in data.items():
            update_key = f"update_{key}"
            self.fields[update_key] = forms.BooleanField(
                required=False,
                label=f"Update {key} from {getattr(instance, key)} to {value}",
            )

            self.fields[key] = forms.CharField(initial=value, required=False)
            self.fields[key].widget = self.fields[key].hidden_widget()
        self.helper = FormHelper()
        self.helper.add_input(Submit("submit", "Submit"))
