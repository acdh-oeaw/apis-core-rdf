from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit
from django import forms
from django.contrib.contenttypes.models import ContentType
from django.urls import reverse
from django.utils.http import urlencode
from django.utils.translation import gettext_lazy as _

from apis_core.core.fields import ApisListSelect2
from apis_core.generic.forms import GenericFilterSetForm, GenericModelForm
from apis_core.generic.forms.fields import ModelImportChoiceField


class RelationForm(GenericModelForm):
    """
    This form overrides generic form for relation editing.
    Relations have generic relations to subj and obj, but we
    hide those ForeignKey form fields and instead show
    autocomplete choices fields.
    In addition, one can pass a hx_post_route argument to the
    form to make the form set the `hx-post` attribute to the
    given value.
    We also pass a `reverse` boolean, wich gets passed on
    to the htmx POST endpoint using url parameters (the endpoint
    can then select the success_url based on the `reverse` state).
    """

    class Media:
        js = ["js/relation_dialog.js"]

    class Meta:
        fields = "__all__"

    def __init__(self, *args, **kwargs):
        """
        Initialize the form and replace `subj_object_id` and
        `obj_object_id` fields with a autocomplete widget.
        """

        self.params = kwargs.pop("params", {})
        subj_model = getattr(self.Meta.model, "subj_model", None)
        obj_model = getattr(self.Meta.model, "obj_model", None)

        if subj_model:
            subj_ct = ContentType.objects.get_for_model(subj_model)
            kwargs["initial"]["subj_content_type"] = subj_ct
        if obj_model:
            obj_ct = ContentType.objects.get_for_model(obj_model)
            kwargs["initial"]["obj_content_type"] = obj_ct

        super().__init__(*args, **kwargs)

        if subj_model:
            self.fields["subj_content_type"].required = False
            self.fields["subj_content_type"].widget = forms.HiddenInput()
            # if we already now the id of the subject, hide the subject input
            if kwargs["initial"].get("subj_object_id"):
                self.fields["subj_object_id"].widget = forms.HiddenInput()
            # otherwise create an autocomplete to select the subject
            else:
                self.fields["subj_object_id"] = ModelImportChoiceField(
                    queryset=subj_model.objects.all(), label=_("Subject")
                )
                self.fields["subj_object_id"].widget = ApisListSelect2(
                    attrs={"data-html": True},
                    url=reverse("apis_core:generic:autocomplete", args=[subj_ct])
                    + "?create=True",
                )
                self.fields["subj_object_id"].widget.choices = self.fields[
                    "subj_object_id"
                ].choices

        if obj_model:
            self.fields["obj_content_type"].required = False
            self.fields["obj_content_type"].widget = forms.HiddenInput()
            # if we already now the id of the object, hide the object input
            if kwargs["initial"].get("obj_object_id"):
                self.fields["obj_object_id"].widget = forms.HiddenInput()
            # otherwise create an autocomplete to select the object
            else:
                self.fields["obj_object_id"] = ModelImportChoiceField(
                    queryset=obj_model.objects.all(), label=_("Object")
                )
                self.fields["obj_object_id"].widget = ApisListSelect2(
                    attrs={"data-html": True},
                    url=reverse("apis_core:generic:autocomplete", args=[obj_ct])
                    + "?create=True",
                )
                self.fields["obj_object_id"].widget.choices = self.fields[
                    "obj_object_id"
                ].choices

        self.order_fields(self.field_order)
        self.helper = FormHelper(self)
        model_ct = ContentType.objects.get_for_model(self.Meta.model)
        self.helper.form_id = f"relation_{model_ct.model}_form"
        self.helper.add_input(Submit("submit", "Submit"))

        if hx_post_route := self.params.get("hx_post_route", False):
            self.helper.attrs = {
                "hx-post": hx_post_route + "?" + urlencode(self.params, doseq=True),
                "hx-swap": "outerHTML",
                "hx-target": f"#{self.helper.form_id}",
            }

    def clean(self) -> dict:
        """
        subj_object_id and obj_object_id can either come
        from initial values or from the autocomplete.
        In the former case, the values are simply the primary keys,
        which is what we want.
        In the latter case, the values are object instances and we
        want to set them to the primary keys instead.
        """
        cleaned_data = super().clean()
        subj_object_id = cleaned_data.get("subj_object_id")
        if subj_object_id and not isinstance(subj_object_id, int):
            cleaned_data["subj_object_id"] = subj_object_id.id
        obj_object_id = cleaned_data.get("obj_object_id")
        if obj_object_id and not isinstance(obj_object_id, int):
            cleaned_data["obj_object_id"] = obj_object_id.id
        return cleaned_data

    @property
    def relation_name(self) -> str:
        """A helper method to access the correct name of the relation"""
        if self.params["reverse"]:
            return self._meta.model.reverse_name
        return self._meta.model.name


class RelationFilterSetForm(GenericFilterSetForm):
    """
    FilterSet form for relations based on GenericFilterSetForm.
    Excludes `relation_ptr` from the columns selector
    """

    columns_exclude = ["relation_ptr"]
