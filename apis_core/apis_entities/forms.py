# -*- coding: utf-8 -*-
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Fieldset, Field
from crispy_forms.layout import Submit
from dal import autocomplete
from django import forms
from django.conf import settings
from django.core.validators import URLValidator
from django.urls import reverse

from apis_core.apis_metainfo.models import Uri, Collection
from apis_core.utils import DateParser, caching, settings as apis_settings
from apis_core.utils.settings import get_entity_settings_by_modelname
from .fields import ListSelect2


class SearchForm(forms.Form):
    search = forms.CharField(label="Search")

    @property
    def helper(self):
        helper = FormHelper()
        helper.form_id = "searchForm"
        helper.form_tag = False
        helper.add_input(Submit("fieldn", "search"))
        helper.form_method = "GET"
        return helper


def get_entities_form(entity):
    """
    Form for edit view for an entity object.

    :param entity: entity name as String
    :return: GenericEntitiesForm class
    """

    if form := apis_settings.get_entity_settings_by_modelname(entity).get("form"):
        return form

    class GenericEntitiesForm(forms.ModelForm):
        class Meta:
            model = caching.get_entity_class_of_name(entity)

            exclude = [
                "start_date",
                "start_start_date",
                "start_end_date",
                "start_date_is_exact",
                "end_date",
                "end_start_date",
                "end_end_date",
                "end_date_is_exact",
                "text",
                "source",
                "published",
                "self_contenttype",
            ]
            # exclude.extend(model.get_related_entity_field_names())
            # exclude.extend(model.get_related_relationtype_field_names())

        def __init__(self, *args, **kwargs):
            super(GenericEntitiesForm, self).__init__(*args, **kwargs)
            self.helper = FormHelper()
            self.helper.form_class = entity.title() + "Form"
            self.helper.form_tag = False
            self.helper.help_text_inline = True
            main_fields = []  # fields to display for entity
            crispy_main_fields = Fieldset(
                f"Entity type: {entity.title()}"
            )  # crispy forms field collection for entity fields

            for f in self.fields.keys():
                main_fields.append(f)

            def sort_fields_list(field_names, entity_name):
                """
                Sorts an entity's field names based on the form_order setting
                defined in the entity's class (if available).
                Field names included in form_order are listed first, followed
                by the remaining field names.

                :param field_names: a list of strings
                :param entity_name: string representation of an entity name
                :return: a list of strings
                """
                entity_settings = get_entity_settings_by_modelname(entity_name)
                form_order = entity_settings.get("form_order", [])

                if len(form_order) > 0:
                    remaining = set(field_names) - set(form_order)
                    field_names = form_order + list(remaining)

                return field_names

            for field in sort_fields_list(main_fields, entity):
                crispy_main_fields.append(Field(field))

            self.helper.layout = Layout(crispy_main_fields)

    return GenericEntitiesForm


class GenericEntitiesStanbolForm(forms.Form):
    def save(self, *args, **kwargs):
        form_uri = self.cleaned_data["entity"]
        uri, _ = Uri.objects.get_or_create(uri=form_uri)
        return uri.root_object

    def __init__(self, entity, *args, **kwargs):

        attrs = {
            "data-placeholder": "Type to get suggestions",
            "data-minimum-input-length": getattr(settings, "APIS_MIN_CHAR", 3),
            "data-html": True,
            "style": "width: auto",
        }
        ent_merge_pk = kwargs.pop("ent_merge_pk", False)
        super(GenericEntitiesStanbolForm, self).__init__(*args, **kwargs)
        self.entity = entity
        self.helper = FormHelper()
        form_kwargs = {"entity": entity}
        url = reverse(
            "apis:apis_entities:generic_entities_autocomplete",
            args=[entity.title(), "remove"],
        )
        label = "Create {} from reference resources".format(entity.title())
        button_label = "Create"
        if ent_merge_pk:
            form_kwargs["ent_merge_pk"] = ent_merge_pk
            url = reverse(
                "apis:apis_entities:generic_entities_autocomplete",
                args=[entity.title(), ent_merge_pk],
            )
            label = "Search for {0} in reference resources or db".format(entity.title())
            button_label = "Merge"
        self.helper.form_action = reverse(
            "apis:apis_entities:generic_entities_stanbol_create", kwargs=form_kwargs
        )
        self.helper.add_input(Submit("submit", button_label))
        self.fields["entity"] = autocomplete.Select2ListCreateChoiceField(
            label=label,
            widget=ListSelect2(url=url, attrs=attrs),
            validators=[URLValidator],
        )


class PersonResolveUriForm(forms.Form):
    # person = forms.CharField(label=False, widget=al.TextWidget('PersonAutocomplete'))
    person = forms.CharField(label=False)
    person_uri = forms.CharField(required=False, widget=forms.HiddenInput())

    def save(self, site_instance, instance=None, commit=True):
        cd = self.cleaned_data
        if cd["person"].startswith("http"):
            uri = Uri.objects.create(uri=cd["person"], entity=site_instance)
        else:
            uri = Uri.objects.create(uri=cd["person_uri"], entity=site_instance)
        return uri

    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop("request", False)
        super(PersonResolveUriForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_tag = False

    def clean(self):
        cleaned_data = super(PersonResolveUriForm, self).clean()
        if Uri.objects.filter(uri=cleaned_data["person_uri"]).exists():
            self.add_error("person", "This Person has already been added to the DB.")
        elif cleaned_data["person"].startswith("http"):
            if Uri.objects.filter(uri=cleaned_data["person"]).exists():
                self.add_error("person", "This URI has already been added to the DB.")


class GenericFilterFormHelper(FormHelper):
    def __init__(self, *args, **kwargs):
        super(GenericFilterFormHelper, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.form_class = "genericFilterForm"
        self.form_method = "GET"
        self.add_input(Submit("Filter", "Filter"))
