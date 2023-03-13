#!/usr/bin/python
# -*- coding: utf-8 -*-
from crispy_forms.helper import FormHelper
from django import forms
from dal import autocomplete
from django.contrib.contenttypes.models import ContentType
from django.db.models import Q
from django.template.loader import render_to_string
from django.urls import reverse
from django.conf import settings

from apis_core.apis_relations.forms2 import validate_target_autocomplete
from apis_core.apis_relations.models import Triple, Property
from apis_core.apis_entities.autocomplete3 import PropertyAutocomplete
from apis_core.apis_relations.tables import (
    render_reification_table,
    render_triple_table,
)
from apis_core.apis_entities.models import AbstractEntity
from apis_core.apis_labels.models import Label
from apis_core.helper_functions import DateParser, caching
from apis_core.helper_functions.RDFParser import RDFParser
from apis_core.apis_entities.fields import ListSelect2, Select2Multiple
from apis_core.helper_functions.caching import get_autocomplete_property_choices


# TODO RDF: Check if this should be removed or adapted
class EntityLabelForm(forms.ModelForm):
    class Meta:
        model = Label
        fields = [
            "label",
            "isoCode_639_3",
            "label_type",
            "start_date_written",
            "end_date_written",
        ]

    def save(self, site_instance, instance=None, commit=True):
        cd = self.cleaned_data
        if instance:
            x = Label.objects.get(pk=instance)
            x.label = cd["label"]
            x.isoCode_639_3 = cd["isoCode_639_3"]
            x.label_type = cd["label_type"]
            x.start_date_written = cd["start_date_written"]
            x.end_date_written = cd["end_date_written"]
        else:
            x = super(EntityLabelForm, self).save(commit=False)
            x.temp_entity = site_instance
        x.save()
        return x

    def __init__(self, siteID=None, *args, **kwargs):
        entity_type = kwargs.pop("entity_type", False)
        self.request = kwargs.pop("request", False)
        super(EntityLabelForm, self).__init__(*args, **kwargs)
        self.fields["label"].required = True
        self.fields["label_type"].required = True
        self.helper = FormHelper()
        self.helper.form_class = "EntityLabelForm"
        self.helper.form_tag = False

        instance = getattr(self, "instance", None)
        if instance != None:

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


# This function here should serve as an example best-practice implementation of ajax logic within
# APIS. While it still carries some context-overhead in the surrounding code, it nevertheless
# boils down to a simplified logic flow of ajax like so:
#
#            ┌──────────────────────────────────────────┐
#            │ main renderer (py)                       │
#            │* renders full context                    │
#            └──┬───────────────────────────────────────┘
#               │* calls sub-renderer with context data
#               ▼
#            ┌──────────────────────────────────────────┐
#     ┌─────►│ sub-renderer (py)                        │
#     │      │* processes python and ORM logic          │
#     │      └──┬───────────────────────────────────────┘
#     │         │* injects context data
#     │         │* renders template
#     │         ▼
#     │      ┌──────────────────────────────────────────┐
#     ├─────►│ form (html)                              │
#     │      │* contains surrounding data-carrier-div   │
#     │      │* contains anchor-div for ajax results    │
#     │      └──┬───────────────────────────────────────┘
#     │         │* sends data-carrier-div
#     │         │* sends anchor-div
#     │         ▼
#     │      ┌──────────────────────────────────────────┐
#     │      │ ajax function (JS)                       │
#     │      │* processes data from data-carrier-div    │
#     │      │* contains url route to sub-renderer (py) │
#     │      └──┬───────────────────────────────────────┘
#     │         │* sends prepared data to sub-renderer (py)
#     │         │* injects response from renderer into
#     └─────────┘  anchor-div of form (html)
#
# The most critical parts here are likely the 'data-carrier-div' acting as a tangible data exchange
# between python and JS logic, as well as the 'anchor-div' which pins the dynamic part down.
#
#  In the case of this render_triple_form function it's important to note that the 'data-carrier'
#  div is defined in the surrounding rendering (either 'render_triple_form_and_table' or
#  'render_reification_form') and the form itself is something that is injected into the anchor-div.
#  So, the ajax rendering here and with reification involves two functions:
#  * a surrounding contextual one (defining the data-carrier-div and anchor-div)
#  * the sub render function which handles the thing that is to injected into anchor-div via ajax
#
# It is possible to handle this whole logic with one rendering only as the diagram above displays,
# but in the case of triple and reification forms it was better to split it for re-usability.
def render_triple_form(
    model_self_class_str,
    model_other_class_str,
    model_self_instance=None,
    triple_instance=None,
    should_include_other_entity=True,
    should_include_remove_button=False,
    should_include_create_button=True,
):
    """
    renders the triple form

    :param model_self_class_str: str representation of the main entity class, always referred as
    self, in django's lowercase format
    :param model_other_class_str: str representation of the other entity class, always referred as
    self, in django's lowercase format
    :param model_self_instance: instance of the current main entity in a edit or detail view
    :param triple_instance: instance of triple
    :param should_include_other_entity: In some cases we need to not display the other entity. But
    it's rare, so the default is set to True
    :param should_include_remove_button: In some cases we need to have a button to remove the
    current triple form. But it's rare, so the default is set to False
    :param should_include_create_button: In some cases we don't need to have a button to process a
    triple form on its own. But it's rare, so the default is set to True
    :return: a html rendered string to be integrated into the calling view
    """

    def instantiate_form():
        """
        creates a Form instance with Triple as its model class

        :return: django form instance
        """

        class TripleForm(forms.Form):
            template_name = "apis_relations/triple_form.html"

            def __init__(self, *args, **kwargs):
                super().__init__(*args, **kwargs)
                self.fields["property"] = autocomplete.Select2ListCreateChoiceField(
                    label="property",
                    widget=ListSelect2(
                        url=reverse(
                            "apis:apis_relations:generic_property_autocomplete",
                            kwargs={
                                "entity_self": model_self_class_str,
                                "entity_other": model_other_class_str,
                            },
                        ),
                        attrs={
                            "data-placeholder": "Type to get suggestions",
                            "data-minimum-input-length": getattr(
                                settings, "APIS_MIN_CHAR", 3
                            ),
                            "data-html": True,
                            "style": "width: 100%",
                        },
                    ),
                )
                if should_include_other_entity:
                    self.fields[
                        "entity_other"
                    ] = autocomplete.Select2ListCreateChoiceField(
                        label="entity",
                        widget=ListSelect2(
                            url=reverse(
                                "apis:apis_entities:generic_entities_autocomplete",
                                kwargs={"entity": model_other_class_str},
                            ),
                            attrs={
                                "data-placeholder": "Type to get suggestions",
                                "data-minimum-input-length": getattr(
                                    settings, "APIS_MIN_CHAR", 3
                                ),
                                "data-html": True,
                                "style": "width: 100%",
                            },
                        ),
                    )
                # Check for possible properties between the two classes
                property_initial_choice = get_autocomplete_property_choices(
                    model_self_class_str=model_self_class_str,
                    model_other_class_str=model_other_class_str,
                    search_name_str="",
                )
                # If there is only one possible property, pre-select it
                if len(property_initial_choice) == 1:
                    property_initial_choice = property_initial_choice[0]
                    self.fields["property"].initial = property_initial_choice["id"]
                    self.fields["property"].choices = [
                        (property_initial_choice["id"], property_initial_choice["text"])
                    ]

        return TripleForm()

    def set_initial_values(triple_form):
        """
        If an existing triple is passed, then use it to set initial values of the form it

        :param triple_form: instantiated form
        :return: same form but initialised with values of the triple instance
        """

        # if the surrounding function got passed a triple instance, use it
        if triple_instance is not None:
            # get the right direction of the property with respect to the main entity instance
            # also in the format defined in the autocomplete class
            property = triple_instance.prop
            if model_self_instance == triple_instance.subj:
                property_initial_choice = {
                    # misusing django-autocomplete return format to inject more values than
                    # anticipated. Reasoning explained in get_autocomplete_property_choices
                    "id": f"id:{property.pk}"
                    + f"__direction:{PropertyAutocomplete.SELF_SUBJ_OTHER_OBJ_STR}",
                    "text": property.name,
                }
            elif model_self_instance == triple_instance.obj:
                property_initial_choice = {
                    # misusing django-autocomplete return format to inject more values than
                    # anticipated. Reasoning explained in get_autocomplete_property_choices
                    "id": f"id:{property.pk}"
                    + f"__direction:{PropertyAutocomplete.SELF_OBJ_OTHER_SUBJ_STR}",
                    "text": property.name_reverse,
                }
            # check for wrong value passed to this function
            else:
                raise Exception("unhandled case.")
            triple_form.fields["property"].initial = property_initial_choice["id"]
            triple_form.fields["property"].choices = [
                (property_initial_choice["id"], property_initial_choice["text"])
            ]
            # check if the other entity is to displayed in the form at all
            if should_include_other_entity:
                # get the right other entity instance
                if model_self_instance == triple_instance.subj:
                    model_other_instance = triple_instance.obj
                elif model_self_instance == triple_instance.obj:
                    model_other_instance = triple_instance.subj
                # check for wrong value passed to this function
                else:
                    raise Exception("unhandled case.")
                triple_form.fields[
                    "entity_other"
                ].initial = model_other_instance.uri_set.all()[0]
                triple_form.fields["entity_other"].choices = [
                    (model_other_instance.uri_set.all()[0], model_other_instance.name)
                ]

        return triple_form

    # just a check to verify this function was called correctly
    if triple_instance is not None and model_self_instance is None:
        raise Exception(
            "a triple instance was passed but no corresponding subject or object instance which is needed."
        )
    triple_form = instantiate_form()
    triple_form = set_initial_values(triple_form)
    if triple_instance is not None:
        triple_id = str(triple_instance.pk)
    else:
        triple_id = ""

    return render_to_string(
        template_name=triple_form.template_name,
        context={
            "triple_id": triple_id,
            "triple_form": triple_form,
            "should_include_remove_button": should_include_remove_button,
            "should_include_create_button": should_include_create_button,
        },
    )


def render_triple_form_and_table(
    model_self_class_str,
    model_other_class_str,
    model_self_id_str,
    request,
):
    """
    The main function for rendering both form and table of a triple. This is only called from
    server's static rendering part, never with any ajax call. The ajax calls handle smaller
    elements.

    :param model_self_class_str: str representation of the main entity class, always referred as
    self, in django's lowercase format
    :param model_other_class_str: str representation of the other entity class, always referred as
    self, in django's lowercase format
    :param model_self_id_str: the id of the main entity instance, needed for creating triples
    :param request: the request object, needed for the table for whatever reason. Could not leave
    it out.
    :return: a html rendered string to be integrated into the calling view
    """

    context = {
        "model_self_class": model_self_class_str,
        "model_other_class": model_other_class_str,
        "model_self_id": model_self_id_str,
        "triple_form": render_triple_form(
            model_self_class_str=model_self_class_str,
            model_other_class_str=model_other_class_str,
        ),
        "triple_table": render_triple_table(
            model_self_class_str=model_self_class_str,
            model_other_class_str=model_other_class_str,
            model_self_id_str=model_self_id_str,
            should_be_editable=True,
            request=request,
        ),
    }

    return render_to_string(
        template_name="apis_relations/triple_form_and_table.html", context=context
    )


def render_reification_form(
    model_self_class_str, reification_type_str, model_self_id_str, reification_id_str=""
):
    """
    renders the reification form with a lot of logic to render contained triple forms

    :param model_self_class_str: str representation of the main entity class, always referred as
    self, in django's lowercase format
    :param reification_type_str: str representation of the reification class, always referred as
    self, in django's lowercase format
    :param model_self_id_str: the id of the main entity instance, needed for creating triples
    :param reification_id_str: the id of a reification instance, in case of loading a pre-existing
    one into form for editing
    :return: a html rendered string
    """

    # process necessary context
    reification_class = caching.get_reification_class_of_name(reification_type_str)
    reification_instance = None
    if reification_id_str != "":
        reification_instance = reification_class.objects.get(pk=reification_id_str)
    model_self_class = caching.get_ontology_class_of_name(model_self_class_str)
    model_self_instance = model_self_class.objects.get(pk=model_self_id_str)
    # check for properties from main entity to reification
    allowed_property_list_to_reification = Property.objects.filter(
        Q(
            subj_class=model_self_instance.self_contenttype,
            obj_class=caching.get_contenttype_of_class(reification_class),
        )
        | Q(
            subj_class=caching.get_contenttype_of_class(reification_class),
            obj_class=model_self_instance.self_contenttype,
        )
    )
    # If only one property is allowed, then buttons to add or remove forms will not be rendered
    if len(allowed_property_list_to_reification) == 1:
        should_include_remove_and_add_button = False
    # If multiple properties are allowed, then buttons to add or remove forms will be rendered
    elif len(allowed_property_list_to_reification) > 1:
        should_include_remove_and_add_button = True
    # since we are already checking, why not check for calling this whole function wrongly
    else:
        raise Exception(
            "With no valid property between classes of self and reification this render function "
            "should have never been called in the first place. The code before calling this "
            "function is responsible for only calling it when there are valid properties."
        )

    def instantiate_form():
        """
        creates a Form instance with respect to the reification model class

        :return: django form instance
        """

        class ReificationForm(forms.ModelForm):
            template_name = "apis_relations/reification_form.html"

            class Meta:
                model = reification_class
                exclude = ["name", "self_contenttype"]

        reification_form = ReificationForm()
        # if a reification_instance is passed, use it to populate the form's fields.
        if reification_instance is not None:
            for k in reification_form.fields.keys():
                reification_form.fields[k].initial = getattr(reification_instance, k)

        return reification_form

    def create_triple_form_container_to_reification():
        """
        creates a container that carries potentially several triple forms FROM the main entity TO
        the reification. It might be that there are several properties available. In such a case
        there will be buttons rendered to add or remove triple forms. If only one property is
        allowed, then no buttons to add or remove will be rendered.

        :return: a dictionary containing common meta-data and a list containing potentially several
        triple forms.
        """

        triple_form_to_reification_list = []
        has_loaded_existing_triple = False
        # If there is an existing reification instance, use it to populate the triples FROM main
        # entity TO the reification
        if reification_instance is not None:
            triple_list = Triple.objects.filter(
                Q(subj=model_self_instance, obj=reification_instance)
                | Q(subj=reification_instance, obj=model_self_instance)
            )
            for triple in triple_list:
                triple_form_to_reification_list.append(
                    render_triple_form(
                        model_self_class_str=model_self_class_str,
                        model_other_class_str=reification_type_str,
                        model_self_instance=model_self_instance,
                        triple_instance=triple,
                        should_include_other_entity=False,
                        should_include_remove_button=should_include_remove_and_add_button,
                        should_include_create_button=False,
                    )
                )
                has_loaded_existing_triple = True
        # If no pre-existing triple was used, create a blank form
        if not has_loaded_existing_triple:
            triple_form_to_reification_list.append(
                render_triple_form(
                    model_self_class_str=model_self_class_str,
                    model_other_class_str=reification_type_str,
                    should_include_other_entity=False,
                    should_include_remove_button=should_include_remove_and_add_button,
                    should_include_create_button=False,
                )
            )

        return {
            "triple_form_to_reification": triple_form_to_reification_list,
            "model_self_class": model_self_class_str,
            "reification_type": reification_type_str,
            "model_self_id": model_self_id_str,
        }

    def create_triple_form_container_from_reification_list():
        """
        creates a container that carries potentially several triple forms FROM the reification TO
        the other entities. Since arbitrary other entities can be related here, buttons will be
        rendered to add or remove triple forms

        :return: a list of dictionaries where each dictionary contains common meta-data and a list
        containing potentially several triple forms.
        """

        entity_type_reification_contenttype = caching.get_contenttype_of_class(
            reification_class
        )
        # Properties are checked for which other entity classes are allowed FROM reification TO them
        related_ct_list = ContentType.objects.filter(
            Q(property_set_obj__subj_class=entity_type_reification_contenttype)
            | Q(property_set_subj__obj_class=entity_type_reification_contenttype)
        ).distinct()
        related_class_list = [ct.model_class() for ct in related_ct_list]
        # main return list
        triple_form_container_from_reification_list = []
        # get potentially pre-existing triples related to this reification
        if reification_instance is not None:
            triple_list = Triple.objects.filter(
                Q(subj=reification_instance) | Q(obj=reification_instance)
            )
        else:
            triple_list = None
        # iterate over all possibly relatable classes and generate triple form containers for each
        for related_class in related_class_list:
            has_loaded_existing_triple = False
            triple_form_from_reification_list = []
            # If there are existing triples, use them to populate the forms
            if triple_list is not None and len(triple_list) > 0:
                for triple in triple_list:
                    if (
                        triple.subj.__class__ is related_class
                        or triple.obj.__class__ is related_class
                    ):
                        if triple.subj == reification_instance:
                            model_other_instance = triple.obj
                        elif triple.obj == reification_instance:
                            model_other_instance = triple.subj
                        else:
                            raise Exception(
                                "this should not happen. Check that the correct triples are "
                                "filtered beforehand."
                            )
                        # exclude the case where entity is the current main entity
                        if str(model_other_instance.pk) != model_self_id_str:
                            triple_form_from_reification_list.append(
                                render_triple_form(
                                    model_self_class_str=reification_type_str,
                                    model_other_class_str=related_class.__name__.lower(),
                                    model_self_instance=reification_instance,
                                    triple_instance=triple,
                                    should_include_remove_button=True,
                                    should_include_create_button=False,
                                )
                            )
                            has_loaded_existing_triple = True
            # If it was not the case that an existing triple was used to populate the form, create
            # a blank one
            if not has_loaded_existing_triple:
                triple_form_from_reification_list.append(
                    render_triple_form(
                        model_self_class_str=reification_type_str,
                        model_other_class_str=related_class.__name__.lower(),
                        should_include_remove_button=True,
                        should_include_create_button=False,
                    )
                )
            triple_form_container_from_reification_list.append(
                {
                    "triple_form_from_reification": triple_form_from_reification_list,
                    "reification_type": reification_type_str,
                    "model_other_class": related_class.__name__.lower(),
                    "model_self_id": reification_id_str,
                }
            )

        return triple_form_container_from_reification_list

    reification_form = instantiate_form()
    context = {
        "model_self_id": model_self_id_str,
        "entity_type_reification_str": reification_type_str,
        "reification_id": reification_id_str,
        "reification_form": reification_form,
        "triple_form_container_to_reification": create_triple_form_container_to_reification(),
        "triple_form_container_from_reification_list": create_triple_form_container_from_reification_list(),
        "should_include_add_button": should_include_remove_and_add_button,
    }
    result_rendered = render_to_string(
        template_name=reification_form.template_name,
        context=context,
    )

    return result_rendered


def render_reification_form_and_table(
    model_self_class_str,
    reification_type_str,
    model_self_id_str,
    request,
):
    """
    The main function for rendering both form and table of a reification. This is only called from
    server's static rendering part, never with any ajax call. The ajax calls handle smaller
    elements.

    :param model_self_class_str: str representation of the main entity class, always referred as
    self, in django's lowercase format
    :param reification_type_str: str representation of the reification class, always referred as
    self, in django's lowercase format
    :param model_self_id_str: the id of the main entity instance, needed for creating triples
    :param request: the request object, needed for the table for whatever reason. Could not leave
    it out.
    :return: a html rendered string to be integrated into the calling view
    """

    context = {
        "model_self_class": model_self_class_str,
        "model_self_id": model_self_id_str,
        "reification_type": reification_type_str,
        "reification_form": render_reification_form(
            model_self_class_str=model_self_class_str,
            reification_type_str=reification_type_str,
            model_self_id_str=model_self_id_str,
        ),
        "reification_table": render_reification_table(
            reification_type_str=reification_type_str,
            model_self_class_str=model_self_class_str,
            model_self_id_str=model_self_id_str,
            should_be_editable=True,
            request=request,
        ),
    }

    return render_to_string(
        template_name="apis_relations/reification_form_and_table.html",
        context=context,
    )
