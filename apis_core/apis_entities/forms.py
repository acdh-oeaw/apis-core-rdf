# -*- coding: utf-8 -*-
from crispy_forms.bootstrap import Accordion, AccordionGroup
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Fieldset, Field
from crispy_forms.layout import Submit
from dal import autocomplete
from django import forms
from django.conf import settings
from django.contrib.contenttypes.models import ContentType
from django.core.validators import URLValidator
from django.db.models.fields import BLANK_CHOICE_DASH
from django.forms import ModelMultipleChoiceField, ModelChoiceField
from django.urls import reverse

from apis_core.apis_metainfo.models import Uri, Collection
from apis_core.utils import DateParser, caching, settings as apis_settings
from apis_core.utils.settings import get_entity_settings_by_modelname
from .fields import ListSelect2, Select2Multiple


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
            attrs = {
                "data-placeholder": "Type to get suggestions",
                "data-minimum-input-length": getattr(settings, "APIS_MIN_CHAR", 3),
                "data-html": True,
            }

            for f in self.fields.keys():
                if isinstance(
                    self.fields[f], (ModelMultipleChoiceField, ModelChoiceField)
                ):
                    model_uri = self.fields[f].queryset.model.__name__.lower()

                    if isinstance(self.fields[f], ModelMultipleChoiceField):
                        widget1 = Select2Multiple
                    else:
                        widget1 = ListSelect2

                    matching_content_type = ContentType.objects.filter(
                        app_label__in=[
                            "apis_entities",
                            "apis_metainfo",
                            "apis_relations",
                            "apis_vocabularies",
                        ],
                        model=model_uri,
                    )
                    if (
                        len(matching_content_type) == 1
                        and matching_content_type[0].app_label.lower()
                        == "apis_vocabularies"
                    ):
                        self.fields[f].widget = widget1(
                            url=reverse(
                                "apis:apis_vocabularies:generic_vocabularies_autocomplete",
                                kwargs={"vocab": model_uri, "direct": "normal"},
                            ),
                            attrs=attrs,
                        )
                        if self.instance:
                            res = []
                            if isinstance(self.fields[f], ModelMultipleChoiceField):
                                try:
                                    for x in getattr(self.instance, f).all():
                                        res.append((x.pk, x.label))
                                except ValueError:
                                    pass
                                self.fields[f].initial = res
                                self.fields[f].choices = res
                            else:
                                try:
                                    res = getattr(self.instance, f)
                                    if res is not None:
                                        self.fields[f].initial = (res.pk, res.label)
                                        self.fields[f].choices = [
                                            (res.pk, res.label),
                                        ]
                                except ValueError:
                                    res = ""

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
            # backwards compatibility:
            # those fields are part of TempEntityClass - this
            # block can probably be removed when TempEntityClass
            # is gone from apis_entities
            # for now we at least check if they exist
            if "status" in self.fields:
                self.fields["status"].required = False
            if "collection" in self.fields:
                self.fields["collection"].required = False
            if "start_date_written" in self.fields:
                self.fields["start_date_written"].required = False
            if "end_date_written" in self.fields:
                self.fields["end_date_written"].required = False

            instance = getattr(self, "instance", None)
            if instance != None:

                # same as above, part of TempEntityClass
                if "start_date_written" in self.fields:
                    if instance.start_date_written:
                        self.fields[
                            "start_date_written"
                        ].help_text = DateParser.get_date_help_text_from_dates(
                            single_date=instance.start_date,
                            single_start_date=instance.start_start_date,
                            single_end_date=instance.start_end_date,
                            single_date_written=instance.start_date_written,
                        )
                    else:
                        self.fields[
                            "start_date_written"
                        ].help_text = DateParser.get_date_help_text_default()

                # same as above, part of TempEntityClass
                if "end_date_written" in self.fields:
                    if instance.end_date_written:
                        self.fields[
                            "end_date_written"
                        ].help_text = DateParser.get_date_help_text_from_dates(
                            single_date=instance.end_date,
                            single_start_date=instance.end_start_date,
                            single_end_date=instance.end_end_date,
                            single_date_written=instance.end_date_written,
                        )
                    else:
                        self.fields[
                            "end_date_written"
                        ].help_text = DateParser.get_date_help_text_default()

        def save(self, *args, **kwargs):
            obj = super(GenericEntitiesForm, self).save(*args, **kwargs)

            # backwards compatibility
            # collection is a field of TempEntityClass - this block
            # can be removed when TempEntityClass is gone from apis_entities
            # for now we at least check if the attribute exist
            if hasattr(obj, "collection"):
                if obj.collection.all().count() == 0:
                    col_name = getattr(
                        settings, "APIS_DEFAULT_COLLECTION", "manually created entity"
                    )
                    col, created = Collection.objects.get_or_create(name=col_name)
                    obj.collection.add(col)
            return obj

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
        entity_type = kwargs.pop("entity_type", False)
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
