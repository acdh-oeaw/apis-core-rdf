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
from apis_core.apis_relations.models import Triple
from apis_core.apis_entities.autocomplete3 import SELF_SUBJ_OTHER_OBJ_STR, SELF_OBJ_OTHER_SUBJ_STR, \
    get_cached_property_choices
from apis_core.apis_relations.tables import render_reification_table
from apis_core.apis_entities.models import AbstractEntity
from apis_core.apis_labels.models import Label
from apis_core.helper_functions import DateParser
from apis_core.helper_functions.RDFParser import RDFParser
from apis_core.apis_entities.fields import ListSelect2, Select2Multiple


##############################################
# Generic
##############################################

class EntityLabelForm(forms.ModelForm):

    class Meta:
        model = Label
        fields = ['label', 'isoCode_639_3', 'label_type', 'start_date_written', 'end_date_written']

    def save(self, site_instance, instance=None, commit=True):
        cd = self.cleaned_data
        if instance:
            x = Label.objects.get(pk=instance)
            x.label = cd['label']
            x.isoCode_639_3 = cd['isoCode_639_3']
            x.label_type = cd['label_type']
            x.start_date_written = cd['start_date_written']
            x.end_date_written = cd['end_date_written']
        else:
            x = super(EntityLabelForm, self).save(commit=False)
            x.temp_entity = site_instance
        x.save()
        return x

    def __init__(self, siteID=None, *args, **kwargs):
        entity_type = kwargs.pop('entity_type', False)
        self.request = kwargs.pop('request', False)
        super(EntityLabelForm, self).__init__(*args, **kwargs)
        self.fields['label'].required = True
        self.fields['label_type'].required = True
        self.helper = FormHelper()
        self.helper.form_class = 'EntityLabelForm'
        self.helper.form_tag = False

        instance = getattr(self, 'instance', None)
        if instance != None:

            if instance.start_date_written:
                self.fields['start_date_written'].help_text = DateParser.get_date_help_text_from_dates(
                    single_date=instance.start_date,
                    single_start_date=instance.start_start_date,
                    single_end_date=instance.start_end_date,
                    single_date_written=instance.start_date_written,
                )
            else:
                self.fields['start_date_written'].help_text = DateParser.get_date_help_text_default()

            if instance.end_date_written:
                self.fields['end_date_written'].help_text = DateParser.get_date_help_text_from_dates(
                    single_date=instance.end_date,
                    single_start_date=instance.end_start_date,
                    single_end_date=instance.end_end_date,
                    single_date_written=instance.end_date_written,
                )
            else:
                self.fields['end_date_written'].help_text = DateParser.get_date_help_text_default()


# __before_rdf_refactoring__
#
# ##############################################
# # Person
# ##############################################
#
#
# class PersonLabelForm(EntityLabelForm):
#     pass
#
# ##############################################
# # Institutions
# ##############################################
#
#
# class InstitutionLabelForm(EntityLabelForm):
#     pass
#
#
# ##############################################
# # Places
# ##############################################
#
# class PlaceLabelForm(EntityLabelForm):
#     pass
#
#
# ##############################################
# # Events
# ##############################################
#
#
# class EventLabelForm(EntityLabelForm):
#     pass
#
#
# ##############################################
# # Entities Base Forms
# #############################################
#
#
# class PlaceEntityForm(forms.Form):
#     # place = forms.CharField(label='Place', widget=al.TextWidget('OrtAutocomplete'))
#     place_uri = forms.CharField(required=False, widget=forms.HiddenInput())
#
#     def save(self, *args, **kwargs):
#         cd = self.cleaned_data
#         pl = Place.get_or_create_uri(cd['place_uri'])
#         if not pl:
#             pl = RDFParser(cd['place_uri'], 'Place').get_or_create()
#         return pl

def render_contextual_triple_form(
    entity_type_self_str,
    entity_type_other_str,
    entity_self_instance=None,
    entity_other_instance=None,
    triple_instance=None,
    entity_id_self_str="",
    should_include_other_entity=True,
):
    
    def instantiate_form():
        
        class GenericContextualTripleForm(forms.Form):
            template_name = "apis_relations/contextual_triple_form_single.html"
            def __init__(self, *args, **kwargs):
                super().__init__(*args, **kwargs)
                self.fields["property"] = autocomplete.Select2ListCreateChoiceField(
                    label='property',
                    widget=ListSelect2(
                        url=reverse(
                            'apis:apis_relations:generic_property_autocomplete',
                            kwargs={"entity_self": entity_type_self_str, "entity_other": entity_type_other_str}
                        ),
                        attrs={
                            'data-placeholder': 'Type to get suggestions',
                            'data-minimum-input-length': getattr(settings, "APIS_MIN_CHAR", 3),
                            'data-html': True,
                            'style': 'width: 100%'
                        },
                    ),
                )
                if should_include_other_entity:
                    self.fields["entity_other"] = autocomplete.Select2ListCreateChoiceField(
                        label='entity',
                        widget=ListSelect2(
                            url=reverse(
                                'apis:apis_entities:generic_entities_autocomplete',
                                kwargs={"entity": entity_type_other_str}
                            ),
                            attrs={
                                'data-placeholder': 'Type to get suggestions',
                                'data-minimum-input-length': getattr(settings, "APIS_MIN_CHAR", 3),
                                'data-html': True,
                                'style': 'width: 100%'
                            },
                        ),
                    )
                property_initial_choice = get_cached_property_choices(
                    entity_type_self_str=entity_type_self_str,
                    entity_type_other_str=entity_type_other_str,
                    search_name_str="",
                )
                if len(property_initial_choice) == 1:
                    property_initial_choice = property_initial_choice[0]
                    self.fields["property"].initial = property_initial_choice["id"]
                    self.fields["property"].choices = [(property_initial_choice["id"], property_initial_choice["text"])]
                    
        return GenericContextualTripleForm()
    
    def set_initial_values(triple_form):
        if triple_instance is not None:
            property = triple_instance.prop
            if entity_self_instance == triple_instance.subj:
                property_initial_choice = {
                    'id': f"id:{property.pk}__direction:{SELF_SUBJ_OTHER_OBJ_STR}", # misuse of the id item as explained above
                    'text': property.name
                }
            elif entity_self_instance == triple_instance.obj:
                property_initial_choice = {
                    'id': f"id:{property.pk}__direction:{SELF_OBJ_OTHER_SUBJ_STR}", # misuse of the id item as explained above
                    'text': property.name_reverse
                }
            else:
                raise Exception("unhandled case.")
            triple_form.fields["property"].initial = property_initial_choice["id"]
            triple_form.fields["property"].choices = [(property_initial_choice["id"], property_initial_choice["text"])]
            if should_include_other_entity:
                if entity_other_instance is None:
                    raise Exception("entity_other_instance missing. Must be passed here for pre-loading triple form.")
                triple_form.fields["entity_other"].initial = entity_other_instance.uri_set.all()[0]
                triple_form.fields["entity_other"].choices = [(entity_other_instance.uri_set.all()[0], entity_other_instance.name)]
                
        return triple_form
    
    triple_form = instantiate_form()
    triple_form = set_initial_values(triple_form)
    triple_id = ""
    if triple_instance is not None:
        triple_id = str(triple_instance.pk)
    
    return render_to_string(
        template_name=triple_form.template_name,
        context={
            "entity_type_self_str": entity_type_self_str,
            "entity_type_other_str": entity_type_other_str,
            "entity_id_self": entity_id_self_str,
            "triple_id": triple_id,
            "contextual_triple_form": triple_form,
        }
    )


def render_reification_form(reification_type_str, entity_type_self_str, entity_id_self_str, reification_id_str=""):
    reification_class = AbstractEntity.get_entity_class_of_name(reification_type_str)
    reification_instance = None
    if reification_id_str != "":
        reification_instance = reification_class.objects.get(pk=reification_id_str)
    entity_self_class = AbstractEntity.get_entity_class_of_name(entity_type_self_str)
    entity_self_instance = entity_self_class.objects.get(pk=entity_id_self_str)
    
    def instantiate_form():
        
        class ReificationForm(forms.ModelForm):
            template_name = "apis_relations/reification_form.html"
            class Meta:
                model = reification_class
                fields = ["name", "start_date"]
        
        reification_form = ReificationForm()
        if reification_instance is not None:
            for k in reification_form.fields.keys():
                reification_form.fields[k].initial = getattr(reification_instance, k)
                
        return reification_form
    
    def create_triple_form_container_to_reification():
        triple_form_to_reification_list = []
        has_loaded_existing_triple = False
        if reification_instance is not None:
            triple_list = Triple.objects.filter(
                Q(subj=entity_self_instance, obj=reification_instance)
                | Q(subj=reification_instance, obj=entity_self_instance)
            )
            for triple in triple_list:
                triple_form_to_reification_list.append(
                    render_contextual_triple_form(
                        entity_type_self_str=entity_type_self_str,
                        entity_type_other_str=reification_type_str,
                        entity_self_instance=entity_self_instance,
                        entity_other_instance=reification_instance,
                        triple_instance=triple,
                        should_include_other_entity=False,
                    )
                )
                has_loaded_existing_triple = True
        if not has_loaded_existing_triple:
            triple_form_to_reification_list.append(
                render_contextual_triple_form(
                    entity_type_self_str=entity_type_self_str,
                    entity_type_other_str=reification_type_str,
                    should_include_other_entity=False,
                )
            )
            
        return {
            "triple_form_to_reification": triple_form_to_reification_list,
            "entity_type_self": entity_type_self_str,
            "reification_type": reification_type_str,
            "entity_id_self": "",
        }
    
    def create_triple_form_container_from_reification_list():
        entity_type_reification_content_type = reification_class.get_content_type()
        related_ct_list = ContentType.objects.filter(
            Q(property_set_obj__subj_class=entity_type_reification_content_type)
            | Q(property_set_subj__obj_class=entity_type_reification_content_type)
        ).distinct()
        related_class_list = [ct.model_class() for ct in related_ct_list]
        triple_form_container_from_reification_list = []
        triple_list = None
        if reification_instance is not None:
            triple_list = Triple.objects.filter(
                Q(subj=reification_instance)
                | Q(obj=reification_instance)
            )
        for related_class in related_class_list:
            has_loaded_existing_triple = False
            triple_form_to_reification_list = []
            if triple_list is not None and len(triple_list) > 0:
                for triple in triple_list:
                    if (
                        triple.subj.__class__ is related_class
                        or triple.obj.__class__ is related_class
                    ):
                        entity_other_instance = None
                        if triple.subj == reification_instance:
                            entity_other_instance = triple.obj
                        elif triple.obj == reification_instance:
                            entity_other_instance = triple.subj
                        else:
                            raise Exception("this should not happen. Check that the correct triples are filtered beforehand.")
                        if str(entity_other_instance.pk) != entity_id_self_str:
                            triple_form_to_reification_list.append(
                                render_contextual_triple_form(
                                    entity_type_self_str=reification_type_str,
                                    entity_type_other_str=related_class.__name__.lower(),
                                    entity_self_instance=reification_instance,
                                    entity_other_instance=entity_other_instance,
                                    triple_instance=triple,
                                )
                            )
                            has_loaded_existing_triple = True
            if not has_loaded_existing_triple:
                triple_form_to_reification_list.append(
                    render_contextual_triple_form(
                        entity_type_self_str=reification_type_str,
                        entity_type_other_str=related_class.__name__.lower(),
                    )
                )
            triple_form_container_from_reification_list.append({
                "triple_form_from_reification": triple_form_to_reification_list,
                "reification_type": reification_type_str,
                "entity_type_other": related_class.__name__.lower(),
                "entity_id_self": "",
            })
            
        return triple_form_container_from_reification_list
    
    reification_form = instantiate_form()
    context = {
        "entity_id_self": entity_id_self_str,
        "entity_type_reification_str": reification_type_str,
        "reification_id": reification_id_str,
        "reification_form": reification_form,
        "triple_form_container_to_reification": create_triple_form_container_to_reification(),
        "triple_form_container_from_reification_list": create_triple_form_container_from_reification_list(),
    }
    result_rendered = render_to_string(
        template_name=reification_form.template_name,
        context=context,
    )
    
    return result_rendered

def render_reification_form_and_table(
    entity_type_self_str,
    reification_type_str,
    entity_id_self_str,
    request,
):
    
    return render_to_string(
        "apis_relations/reification_form_and_table.html",
        context={
            "reification_form": render_reification_form(
                reification_type_str=reification_type_str,
                entity_type_self_str=entity_type_self_str,
                entity_id_self_str=entity_id_self_str,
            ),
            "entity_type_self": entity_type_self_str,
            "reification_type": reification_type_str,
            "entity_id_self": entity_id_self_str,
            "reification_table": render_reification_table(
                request=request,
                reification_type_str=reification_type_str,
                entity_type_self_str=entity_type_self_str,
                entity_id_self_str=entity_id_self_str,
            ),
        },
    )
