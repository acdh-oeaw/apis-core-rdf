from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit
from dal import autocomplete
from django import forms
from django.contrib.contenttypes.models import ContentType
from django.core.exceptions import ValidationError
from django.shortcuts import get_object_or_404
from django.urls import reverse
from django.utils.http import urlencode

from apis_core.generic.forms import GenericModelForm
from apis_core.generic.forms.fields import ModelImportChoiceField


class CustomSelect2ListChoiceField(autocomplete.Select2ListChoiceField):
    """
    We use a custom Select2ListChoiceField in our Relation form,
    because we don't want the form value to be validated. The field
    uses the `choices` setting as a basis for validating, but our
    choices span over multiple querysets, so its easier to simply not
    validate (some validation happens in the `clean` method anyway).
    """

    def validate(self, value):
        if "_" not in value:
            raise ValidationError("please choose a correct value")


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

    class Meta:
        fields = "__all__"
        widgets = {
            "subj_content_type": forms.HiddenInput(),
            "subj_object_id": forms.HiddenInput(),
            "obj_content_type": forms.HiddenInput(),
            "obj_object_id": forms.HiddenInput(),
        }

    def __entities_autocomplete_with_params(self, content_types=[ContentType]) -> str:
        """helper method to generate the entities autocomplete url with contentype parameters"""
        url = reverse("apis_core:apis_entities:autocomplete")
        params = [f"entities={ct.app_label}.{ct.model}" for ct in content_types]
        return url + "?" + "&".join(params)

    def __subj_autocomplete_url(self) -> str:
        """generate the autocomplete url for the subj field, using the subject
        types configured in the relation"""
        subj_content_types = [
            ContentType.objects.get_for_model(model)
            for model in self.Meta.model.subj_list()
        ]
        return self.__entities_autocomplete_with_params(subj_content_types)

    def __obj_autocomplete_url(self) -> str:
        """generate the autocomplete url for the obj field, using the object
        types configured in the relation"""
        obj_content_types = [
            ContentType.objects.get_for_model(model)
            for model in self.Meta.model.obj_list()
        ]
        return self.__entities_autocomplete_with_params(obj_content_types)

    def __init__(self, *args, **kwargs):
        """
        Initialize the form and add the `subj` and `obj` fields using the
        generic apis_entities autocomplete with the correct parameters.
        """

        self.is_reverse = kwargs.pop("reverse", False)
        hx_post_route = kwargs.pop("hx_post_route", False)
        super().__init__(*args, **kwargs)
        subj_content_type = kwargs["initial"].get("subj_content_type", None)
        subj_object_id = kwargs["initial"].get("subj_object_id", None)
        obj_content_type = kwargs["initial"].get("obj_content_type", None)
        obj_object_id = kwargs["initial"].get("obj_object_id", None)

        self.subj_instance, self.obj_instance = None, None
        if instance := kwargs.get("instance"):
            self.subj_instance = instance.subj
            self.obj_instance = instance.obj
        else:
            if subj_content_type and subj_object_id:
                model = get_object_or_404(ContentType, pk=subj_content_type)
                self.subj_instance = get_object_or_404(
                    model.model_class(), pk=subj_object_id
                )
            if obj_content_type and obj_object_id:
                model = get_object_or_404(ContentType, pk=obj_content_type)
                self.obj_instance = get_object_or_404(
                    model.model_class(), pk=obj_object_id
                )

        self.fields["subj_object_id"].required = False
        self.fields["subj_content_type"].required = False
        if not subj_object_id:
            if subj_content_type:
                """ If we know the content type the subject will have, we
                use another autocomplete field that allows us to paste links
                and provides external autocomplete results.
                """
                ct = ContentType.objects.get(pk=subj_content_type)
                self.fields["subj"] = ModelImportChoiceField(
                    queryset=ct.model_class().objects.all()
                )
                self.fields["subj"].widget = autocomplete.ListSelect2(
                    url=reverse("apis_core:generic:autocomplete", args=[ct])
                    + "?create=True"
                )
                self.fields["subj"].widget.choices = self.fields["subj"].choices
            else:
                """ If we don't know the content type, we use a generic autocomplete
                field that autocompletes any content type the relation can have as a
                subject.
                """
                self.fields["subj_ct_and_id"] = CustomSelect2ListChoiceField()
                self.fields["subj_ct_and_id"].widget = autocomplete.ListSelect2(
                    url=self.__subj_autocomplete_url()
                )
                if self.subj_instance:
                    content_type = ContentType.objects.get_for_model(self.subj_instance)
                    select_identifier = f"{content_type.id}_{self.subj_instance.id}"
                    self.fields["subj_ct_and_id"].initial = select_identifier
                    self.fields["subj_ct_and_id"].choices = [
                        (select_identifier, self.subj_instance)
                    ]

        self.fields["obj_object_id"].required = False
        self.fields["obj_content_type"].required = False
        if not obj_object_id:
            if obj_content_type:
                """ If we know the content type the object will have, we
                use another autocomplete field that allows us to paste links
                and provides external autocomplete results.
                """
                ct = ContentType.objects.get(pk=obj_content_type)
                self.fields["obj"] = ModelImportChoiceField(
                    queryset=ct.model_class().objects.all()
                )
                self.fields["obj"].widget = autocomplete.ListSelect2(
                    url=reverse("apis_core:generic:autocomplete", args=[ct])
                    + "?create=True"
                )
                self.fields["obj"].widget.choices = self.fields["obj"].choices
            else:
                """ If we don't know the content type, we use a generic autocomplete
                field that autocompletes any content type the relation can have as a
                object.
                """
                self.fields["obj_ct_and_id"] = CustomSelect2ListChoiceField()
                self.fields["obj_ct_and_id"].widget = autocomplete.ListSelect2(
                    url=self.__obj_autocomplete_url()
                )
                if self.obj_instance:
                    content_type = ContentType.objects.get_for_model(self.obj_instance)
                    select_identifier = f"{content_type.id}_{self.obj_instance.id}"
                    self.fields["obj_ct_and_id"].initial = select_identifier
                    self.fields["obj_ct_and_id"].choices = [
                        (select_identifier, self.obj_instance)
                    ]

        self.order_fields(self.field_order)
        self.helper = FormHelper(self)
        model_ct = ContentType.objects.get_for_model(self.Meta.model)
        self.helper.form_id = f"relation_{model_ct.model}_form"
        self.helper.add_input(Submit("submit", "Submit"))

        if hx_post_route:
            urlparams = kwargs["initial"]
            urlparams["reverse"] = self.is_reverse
            urlparams = {k: v for k, v in urlparams.items() if v}
            self.helper.attrs = {
                "hx-post": hx_post_route + "?" + urlencode(urlparams),
                "hx-swap": "outerHTML",
                "hx-target": f"#{self.helper.form_id}",
            }

    def clean(self) -> dict:
        """
        We check if there are `subj` or `obj` fields in the form data
        and if so, we use the data to create objects for the real fields of
        the Relation
        """
        cleaned_data = super().clean()
        if "subj_ct_and_id" in cleaned_data:
            subj_content_type, subj_object_id = cleaned_data["subj_ct_and_id"].split(
                "_"
            )
            cleaned_data["subj_content_type"] = ContentType.objects.get(
                pk=subj_content_type
            )
            cleaned_data["subj_object_id"] = subj_object_id
            del cleaned_data["subj_ct_and_id"]
        if "obj_ct_and_id" in cleaned_data:
            obj_content_type, obj_object_id = cleaned_data["obj_ct_and_id"].split("_")
            cleaned_data["obj_content_type"] = ContentType.objects.get(
                pk=obj_content_type
            )
            cleaned_data["obj_object_id"] = obj_object_id
            del cleaned_data["obj_ct_and_id"]
        if "subj" in cleaned_data:
            cleaned_data["subj_object_id"] = cleaned_data.pop("subj").id
        if "obj" in cleaned_data:
            cleaned_data["obj_object_id"] = cleaned_data.pop("obj").id
        return cleaned_data

    @property
    def relation_name(self) -> str:
        """A helper method to access the correct name of the relation"""
        if self.is_reverse:
            return self._meta.model.reverse_name
        return self._meta.model.name
