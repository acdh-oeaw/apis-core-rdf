import json
import re
import inspect
from django import forms
from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.contrib.contenttypes.models import ContentType
from django.db.models import Q
from django.http import JsonResponse, HttpResponse, Http404
from django.template.loader import render_to_string
from apis_ontology.models import *
from django.shortcuts import render
from apis_core.apis_entities.models import AbstractEntity
from apis_core.apis_relations import forms as relation_form_module
from apis_core.apis_relations.forms import render_reification_form, render_triple_form
from apis_core.apis_entities.autocomplete3 import PropertyAutocomplete
from apis_core.apis_labels.models import Label
from apis_core.apis_metainfo.models import Uri
from apis_core.apis_relations.models import Property, TempTriple, Triple
from dal import autocomplete
from apis_core.apis_entities.fields import ListSelect2, Select2Multiple
from django.urls import reverse
from .tables import LabelTableEdit, render_reification_table, render_triple_table
from apis_core.helper_functions import caching


form_module_list = [relation_form_module]
if 'apis_highlighter' in settings.INSTALLED_APPS:
    from apis_highlighter.highlighter import highlight_text_new
    from apis_highlighter import forms as highlighter_form_module
    form_module_list.append(highlighter_form_module)


def turn_form_modules_into_dict(form_module_list):
    """
    Since form classes are loaded dynamically from the respective modules and it's settings-dependent which modules
    are imported and which not, it's better to differentiate here which modules are imported close to their imports
    and then providing a dict for later extraction of the required form class.
    """

    form_class_dict = {}
    for m in form_module_list:
        for name, cls in inspect.getmembers(m, inspect.isclass):
            form_class_dict[name] = cls

    return form_class_dict

form_class_dict = turn_form_modules_into_dict(form_module_list)


############################################################################
############################################################################
#
#   Generic views for AjaxForms
#
############################################################################
############################################################################

######################################################
# test for class-ignoring _ajax_form-functions
######################################################


# __before_rdf_refactoring__
#
# Model-classes must be registered together with their ModelForm-classes
# registered_forms = {'WorkWorkForm': [WorkWork, Work, Work],
#                     'PersonPlaceForm': [PersonPlace, Person, Place],
#                     'PersonPlaceHighlighterForm': [PersonPlace, Person, Place],
#                     'PersonPersonForm': [PersonPerson, Person, Person],
#                     'PersonPersonHighlighterForm': [PersonPerson, Person, Person],
#                     'PersonInstitutionForm': [PersonInstitution, Person, Institution],
#                     'PersonEventForm': [PersonEvent, Person, Event],
#                     'PersonWorkForm': [PersonWork, Person, Work],
#                     'PersonInstitutionHighlighterForm': [PersonInstitution, Person, Institution],
#                     'PersonWorkHighlighterForm': [PersonWork, Person, Work],
#                     'PlaceWorkHighlighterForm': [PlaceWork, Place, Work],
#                     'InstitutionWorkHighlighterForm': [InstitutionWork, Institution, Work],
#                     'InstitutionPlaceForm': [InstitutionPlace, Institution, Place],
#                     'InstitutionInstitutionForm': [
#                         InstitutionInstitution,
#                         Institution,
#                         Institution],
#                     'InstitutionPersonForm': [PersonInstitution, Institution, Person],
#                     'InstitutionEventForm': [InstitutionEvent, Institution, Event],
#                     'InstitutionWorkForm': [InstitutionWork, Institution, Work],
#                     'PlaceEventForm': [PlaceEvent, Place, Event],
#                     'PlaceWorkForm': [PlaceWork, Place, Work],
#                     'PlacePlaceForm': [PlacePlace, Place, Place],
#                     'EventWorkForm': [EventWork, Event, Work],
#                     'InstitutionLabelForm': [Label, Institution, Label],
#                     'PersonLabelForm': [Label, Person, Label],
#                     'EventLabelForm': [Label, Event, Label],
#                     'PersonResolveUriForm': [Uri, Person, Uri],
#                     'SundayHighlighterForm': [ ],
#                     'AddRelationHighlighterPersonForm': [],
#                     #'PlaceHighlighterForm': [Annotation, ],
#                     #'PersonHighlighterForm': [Annotation, ]
#                     }



# TODO RDF : Remove
# this function became a hybrid between vanilla ajax logic and rdf triple logic. But it is now fully
# superseded of new ajax logic, so it can be removed. However it probably is still used for
# highlighter. So this needs to looked into and moved to the new ajax logic too.
@login_required
def get_form_ajax(request):
    '''Returns forms rendered in html'''

    # __before_rdf_refactoring__
    #
    # FormName = request.POST.get('FormName')
    # SiteID = request.POST.get('SiteID')
    # ButtonText = request.POST.get('ButtonText')
    # ObjectID = request.POST.get('ObjectID')
    # entity_type_str = request.POST.get('entity_type')
    # form_match = re.match(r'([A-Z][a-z]+)([A-Z][a-z]+)(Highlighter)?Form', FormName)
    # form_match2 = re.match(r'([A-Z][a-z]+)(Highlighter)?Form', FormName)
    # if FormName and form_match:
    #     entity_type_v1 = ContentType.objects.filter(
    #         model='{}{}'.format(form_match.group(1).lower(), form_match.group(2)).lower(),
    #         app_label='apis_relations')
    #     entity_type_v2 = ContentType.objects.none()
    # elif FormName and form_match2:
    #     entity_type_v2 = ContentType.objects.filter(
    #         model='{}'.format(
    #             form_match.group(1).lower(),
    #             app_label='apis_entities'))
    #     entity_type_v1 = ContentType.objects.none()
    # else:
    #     entity_type_v1 = ContentType.objects.none()
    #     entity_type_v2 = ContentType.objects.none()
    # if ObjectID == 'false' or ObjectID is None or ObjectID == 'None':
    #     ObjectID = False
    #     form_dict = {'entity_type': entity_type_str}
    # elif entity_type_v1.count() > 0:
    #     d = entity_type_v1[0].model_class().objects.get(pk=ObjectID)
    #     form_dict = {'instance': d, 'siteID': SiteID, 'entity_type': entity_type_str}
    # elif entity_type_v2.count() > 0:
    #     d = entity_type_v2[0].model_class().objects.get(pk=ObjectID)
    #     form_dict = {'instance': d, 'siteID': SiteID, 'entity_type': entity_type_str}
    # else:
    #     if FormName not in registered_forms.keys():
    #         raise Http404
    #     d = registered_forms[FormName][0].objects.get(pk=ObjectID)
    #     form_dict = {'instance': d, 'siteID': SiteID, 'entity_type': entity_type_str}
    # if entity_type_v1.count() > 0:
    #     form_dict['relation_form'] = '{}{}'.format(form_match.group(1), form_match.group(2))
    #     if form_match.group(3) == 'Highlighter':
    #         form_dict['highlighter'] = True
    #     form = GenericRelationForm(**form_dict)
    # else:
    #     form_class = form_class_dict[FormName]
    #     form = form_class(**form_dict)
    #
    # __after_rdf_refactoring__
    form_name = request.POST.get('FormName')
    SiteID = int(request.POST.get('SiteID'))
    ButtonText = request.POST.get('ButtonText')
    ObjectID = request.POST.get('ObjectID')
    model_self_class_str = request.POST.get('entity_type')


    if ObjectID is None and form_name.startswith("triple_form_"):
        # If this is the case, then instantiate an empty form

        model_other_class_str = form_name.split("_to_")[1]

        form = GenericTripleForm(
            model_self_class_str=model_self_class_str,
            model_other_class_str=model_other_class_str,
        )

    elif ObjectID is not None and SiteID is not None:
        # If this is the case, then instantiate a form and pre-load with existing data

        triple = TempTriple.objects.get(pk=ObjectID)
        property_instance = triple.prop

        if triple.subj.pk == SiteID:
            entity_instance_self = triple.subj
            entity_instance_other = triple.obj
            property_direction = PropertyAutocomplete.SELF_SUBJ_OTHER_OBJ_STR
        elif triple.obj.pk == SiteID:
            entity_instance_self = triple.obj
            entity_instance_other = triple.subj
            property_direction = PropertyAutocomplete.SELF_OBJ_OTHER_SUBJ_STR
        else:
            raise Exception("SiteID was not found in triple")

        model_other_class_str = entity_instance_other.__class__.__name__
        model_self_class_str = entity_instance_self.__class__.__name__
        form_name = f"triple_form_{model_self_class_str.lower()}_to_{model_other_class_str.lower()}"

        form = GenericTripleForm(
            model_self_class_str=model_self_class_str,
            model_other_class_str=model_other_class_str,
        )
        form.load_subj_obj_prop(
            entity_instance_self,
            entity_instance_other,
            property_instance,
            property_direction,
        )
        form.load_remaining_data_from_triple(triple)

    else:

        raise Exception("Missing necessary form data")

    # __before_rdf_refactoring__
    #
    # tab = FormName[:-4]
    # data = {'tab': tab, 'form': render_to_string("apis_relations/_ajax_form.html", {
    #             "entity_type": entity_type_str,
    #             "form": form,
    #             'type1': FormName,
    #             'url2': 'save_ajax_'+FormName,
    #             'button_text': ButtonText,
    #             'ObjectID': ObjectID,
    #             'SiteID': SiteID})}
    #
    # return HttpResponse(json.dumps(data), content_type='application/json')
    #
    # __after_rdf_refactoring__
    param_dict = {
        "entity_type": model_self_class_str,
        "form": form,
        'type1': form_name,
        'url2': 'save_ajax_'+ form_name,
        'button_text': ButtonText,
        'ObjectID': ObjectID,
        'SiteID': SiteID,
    }

    rendered_form_str = render_to_string(
        "apis_relations/_ajax_form.html", # rel_form_logic_breadcrumb (for refinding the implicit connections)
        context=param_dict
    )

    data = {
        'tab': form_name,
        'form': rendered_form_str
    }

    return HttpResponse(json.dumps(data), content_type='application/json')


# TODO RDF : Implement highlighter and label form
# TODO RDF : Check if rdf refactoring covers all use cases
@login_required
def save_ajax_form(request, entity_type, kind_form, SiteID, ObjectID=False): # rel_form_logic_breadcrumb (for refinding the implicit connections)
    '''Tests validity and saves AjaxForms, returns them when validity test fails'''

    # __before_rdf_refactoring__
    #
    # if kind_form not in registered_forms.keys():
    #     raise Http404
    #
    # button_text = "create/modify"
    #
    # if not ObjectID:
    #     instance_id = ''
    # else:
    #     instance_id = ObjectID
    # entity_type_str = entity_type
    # entity_type = caching.get_ontology_class_of_name(entity_type)
    #
    # form_match = re.match(r'([A-Z][a-z]+)([A-Z][a-z]+)?(Highlighter)?Form', kind_form)
    # form_dict = {'data': request.POST,
    #              'entity_type': entity_type,
    #              'request': request}
    #
    #
    # test_form_relations = ContentType.objects.filter(
    #     model='{}{}'.format(form_match.group(1).lower(), form_match.group(2)).lower(),
    #     app_label='apis_relations')
    # tab = re.match(r'(.*)Form', kind_form).group(1)
    # call_function = 'EntityRelationForm_response'
    # if test_form_relations.count() > 0:
    #     relation_form = test_form_relations[0].model_class()
    #     form_dict['relation_form'] = relation_form
    #     if form_match.group(3) == 'Highlighter':
    #         form_dict['highlighter'] = True
    #         tab = form_match.group(1)+form_match.group(2)
    #         call_function = 'HighlForm_response'
    #     form = GenericRelationForm(**form_dict)
    # else:
    #     form_class = form_class_dict[kind_form]
    #     form = form_class(**form_dict)
    #
    # __after_rdf_refactoring__
    self_other = kind_form.split("triple_form_")[1].split("_to_")
    model_self_class_str = self_other[0]
    model_other_class_str = self_other[1]
    model_self_class = caching.get_ontology_class_of_name(model_self_class_str)
    model_other_class_class = caching.get_ontology_class_of_name(model_other_class_str)
    entity_instance_self = model_self_class.objects.get(pk=SiteID)
    entity_instance_other = model_other_class_class.get_or_create_uri(uri=request.POST["other_entity"])
    start_date_written =request.POST["start_date_written"]
    end_date_written =request.POST["end_date_written"]
    property_param_dict = {}
    for param_pair in request.POST["property"].split("__"):
        param_pair_split = param_pair.split(":")
        property_param_dict[param_pair_split[0]] = param_pair_split[1]
    property_instance = Property.objects.get(pk=property_param_dict["id"])
    property_direction = property_param_dict["direction"]

    form = GenericTripleForm(model_self_class_str, model_other_class_str)
    form.load_subj_obj_prop(
        entity_instance_self,
        entity_instance_other,
        property_instance,
        property_direction,
    )

    if ObjectID is not False:

        triple = TempTriple.objects.get(pk=ObjectID)
        form.load_remaining_data_from_triple(triple)

    form.load_remaining_data_from_input(
        start_date_written,
        end_date_written,
    )
    form.save()

    # __before_rdf_refactoring__
    #
    # data = {
    #     'test': False,
    #     'call_function': call_function,
    #         'DivID': 'div_' + kind_form + instance_id,
    #         'form': render_to_string(
    #             "apis_relations/_ajax_form.html", context={
    #                 "entity_type": entity_type_str,
    #                 "form": form,
    #                 'type1': kind_form,
    #                 'url2': 'save_ajax_' + kind_form,
    #                 'button_text': button_text,
    #                 'ObjectID': ObjectID,
    #                 'SiteID': SiteID
    #             },
    #             request=request
    #         )
    # }
    #
    # __after_rdf_refactoring__
    data = {
        'test': True,
        'tab': kind_form,
        'call_function': 'EntityRelationForm_response',
        'instance': form.instance.get_web_object(),
        'table_html': form.get_html_table(entity_instance_self, entity_instance_other).as_html(request),
        'text': None,
        'right_card': True
    }
    return HttpResponse(json.dumps(data), content_type='application/json')

    # __before_rdf_refactoring__
    #
    # if form.is_valid():
    #     site_instance = entity_type.objects.get(pk=SiteID)
    #     set_ann_proj = request.session.get('annotation_project', 1)
    #     entity_types_highlighter = request.session.get('entity_types_highlighter')
    #     users_show = request.session.get('users_show_highlighter', None)
    #     hl_text = None
    #     if ObjectID:
    #         # kommt hier rein, wenn form vorgefertigte Daten hat
    #         instance = form.save(instance=ObjectID, site_instance=site_instance)
    #     else:
    #         # kommt hier rein, wenn form neuen Daten hat
    #         instance = form.save(site_instance=site_instance)
    #     right_card = True
    #     if test_form_relations.count() > 0:
    #         table_html = form.get_html_table(entity_type_str, request, site_instance, form_match)
    #     if 'Highlighter' in tab or form_match.group(3) == 'Highlighter':
    #         hl_text = {
    #             'text': highlight_text_new(form.get_text_id(),
    #                                    users_show=users_show,
    #                                    set_ann_proj=set_ann_proj,
    #                                    types=entity_types_highlighter)[0].strip(),
    #             'id': form.get_text_id()}
    #     if tab == 'PersonLabel':
    #         table_html = LabelTableEdit(
    #                 data=site_instance.label_set.all(),
    #                 prefix='PL-')
    #     elif tab == 'InstitutionLabel':
    #         table_html = LabelTableEdit(
    #                 data=site_instance.label_set.all(),
    #                 prefix='IL-')
    #     elif tab == 'PersonResolveUri':
    #         table_html = EntityUriTable(
    #             Uri.objects.filter(entity=site_instance),
    #             prefix='PURI-'
    #         )
    #
    #     elif tab == 'AddRelationHighlighterPerson' or tab == 'PlaceHighlighter' or tab == 'PersonHighlighter' or tab == 'SundayHighlighter':
    #         table_html = None
    #         right_card = False
    #         call_function = 'PAddRelation_response'
    #         instance = None
    #     if instance:
    #         instance2 = instance.get_web_object()
    #     else:
    #         instance2 = None
    #     if table_html:
    #         table_html2 = table_html.as_html(request)
    #     else:
    #         table_html2 = None
    #     data = {'test': True, 'tab': tab, 'call_function': call_function,
    #             'instance': instance2,
    #             'table_html': table_html2,
    #             'text': hl_text,
    #             'right_card': right_card}
    # else:
    #     if 'Highlighter' in tab:
    #         call_function = 'HighlForm_response'
    #     data = {'test': False, 'call_function': call_function,
    #             'DivID': 'div_'+kind_form+instance_id,
    #             'form': render_to_string("apis_relations/_ajax_form.html", context={
    #                 "entity_type": entity_type_str,
    #                 "form": form, 'type1': kind_form, 'url2': 'save_ajax_'+kind_form,
    #                 'button_text': button_text, 'ObjectID': ObjectID, 'SiteID': SiteID},
    #                 request=request)}
    #

def create_triple_by_form_data(triple_form_data):
    triple = None
    if triple_form_data["triple_id"] != "":
        triple_set = Triple.objects.filter(pk=triple_form_data["triple_id"])
        # There could be the edge-case where a user deleted a triple in the table but its values
        # had been already loaded into the form and the form was posted. In this case we create a
        # new triple. Hence, this len check:
        if len(triple_set) == 0:
            triple = None
        else:
            triple = triple_set[0]
    if triple_form_data["property_id"] != "" and triple_form_data["model_other_id"] != "":
        model_self_class = caching.get_ontology_class_of_name(triple_form_data["model_self_class"])
        model_self_instance = model_self_class.objects.get(pk=triple_form_data["model_self_id"])
        # because we reuse the entity-autocomplete which also queries external resources, we have to
        # fetch entity_other by its URI here
        model_other_uri = Uri.objects.get(uri=triple_form_data["model_other_id"])
        model_other_instance = model_other_uri.root_object
        property = Property.objects.get(pk=triple_form_data["property_id"])
        if triple_form_data["property_direction"] == PropertyAutocomplete.SELF_SUBJ_OTHER_OBJ_STR:
            if triple is not None:
                triple.subj = model_self_instance
                triple.obj = model_other_instance
                triple.prop = property
                triple.save()
            else:
                triple = Triple.objects.get_or_create(
                    subj=model_self_instance,
                    obj=model_other_instance,
                    prop=property
                )[0]
        elif triple_form_data["property_direction"] == PropertyAutocomplete.SELF_OBJ_OTHER_SUBJ_STR:
            if triple is not None:
                triple.subj = model_other_instance
                triple.obj = model_self_instance
                triple.prop = property
                triple.save()
            else:
                triple = Triple.objects.get_or_create(
                    subj=model_other_instance,
                    obj=model_self_instance,
                    prop=property
                )[0]
        else:
            raise Exception("direction missing or invalid.")
        
    return triple
    

def ajax_2_load_triple_form(request):
    
    def parse_boolean_val(request, key):
        val = request.POST.get(key)
        if val is not None and val.lower() == "true":
            return True
        else:
            return False
        
    should_include_other_entity = parse_boolean_val(request, "should_include_other_entity")
    should_include_remove_button = parse_boolean_val(request, "should_include_remove_button")
    should_include_create_button = parse_boolean_val(request, "should_include_create_button")
    model_self_class = caching.get_ontology_class_of_name(request.POST["model_self_class"])
    model_self_id = request.POST["model_self_id"]
    if model_self_id != "":
        model_self_instance = model_self_class.objects.get(pk=request.POST["model_self_id"])
    else:
        model_self_instance = None
    triple_id = request.POST.get("triple_id")
    if triple_id != "":
        triple_instance = Triple.objects.get(pk=triple_id)
    else:
        triple_instance = None
    response = JsonResponse(
        data=render_triple_form(
            model_self_class_str=request.POST["model_self_class"],
            model_other_class_str=request.POST["model_other_class"],
            model_self_instance=model_self_instance,
            triple_instance=triple_instance,
            should_include_other_entity=should_include_other_entity,
            should_include_remove_button=should_include_remove_button,
            should_include_create_button=should_include_create_button,
        ),
        status=200,
        safe=False
    )
    
    return response

def ajax_2_post_triple_form(request):
    create_triple_by_form_data(request.POST)
    response = JsonResponse(
        data={
            "form": render_triple_form(
                model_self_class_str=request.POST["model_self_class"],
                model_other_class_str=request.POST["model_other_class"],
            ),
            "table": render_triple_table(
                model_self_class_str=request.POST["model_self_class"],
                model_other_class_str=request.POST["model_other_class"],
                model_self_id_str=request.POST["model_self_id"],
                should_be_editable=True,
                request=request,
            ),
        },
        status=200,
        safe=False
    )
    
    return response

def ajax_2_delete_triple(request):
    triple_id = request.POST["triple_id"]
    if triple_id != "":
        Triple.objects.get(pk=triple_id).delete()
    response = JsonResponse(
        data=render_triple_table(
            model_self_class_str=request.POST["model_self_class"],
            model_other_class_str=request.POST["model_other_class"],
            model_self_id_str=request.POST["model_self_id"],
            should_be_editable=True,
            request=request,
        ),
        status=200,
        safe=False
    )
    
    return response

def ajax_2_load_reification_form(request):
    response = JsonResponse(
        data=render_reification_form(
            model_self_class_str=request.POST["model_self_class"],
            reification_type_str=request.POST["reification_type"],
            model_self_id_str=request.POST["model_self_id"],
            reification_id_str=request.POST["reification_id"],
        ),
        status=200,
        safe=False
    )

    return response

def ajax_2_post_reification_form(request):
    class FormException(Exception):
        pass
    
    def process_reification_instance(post_data):
        reification_class = caching.get_reification_class_of_name(post_data["reification_type"])
        reification_instance_id = post_data["reification_attr_form"].pop("reification_id")
        if reification_instance_id != "":
            reification_instance = reification_class.objects.get(pk=reification_instance_id)
        else:
            reification_instance = reification_class.objects.create()
        for k, v in post_data["reification_attr_form"].items():
            setattr(reification_instance, k, v)
        reification_instance.save()
        
        return reification_instance
    
    def process_triples_to_reification(reification_instance, triple_form_data_list):
        related_triple_list = []
        valid_property_counter = 0
        for triple_form_data in triple_form_data_list:
            if triple_form_data["property_id"] != "":
                valid_property_counter += 1
        if valid_property_counter == 0:
            raise FormException(
                "A reification without relation from main entity to the reification goes against "
                "the principle of a reification being a dependent instance. Please provide a "
                "relation between the main entity and the reification."
            )
        for triple_form_data in triple_form_data_list:
            if (
                triple_form_data["model_other_id"] != ""
                and triple_form_data["model_other_id"] != str(reification_instance.pk)
            ):
                raise Exception(
                    "A wrong id was passed. The 'entity_other' in this case must be the reification"
                    ", however the reification's id is not equal to the one from 'entity_other'"
                )
            triple_form_data["model_other_id"] = reification_instance.uri_set.first().uri
            triple = create_triple_by_form_data(triple_form_data)
            if triple is not None:
                related_triple_list.append(triple)

        return related_triple_list
            
    def process_triples_from_reification(reification_instance, triple_form_data_list):
        related_triple_list = []
        for triple_form_data in triple_form_data_list:
            if (
                triple_form_data["model_self_id"] != ""
                and triple_form_data["model_self_id"] != str(reification_instance.pk)
            ):
                raise Exception(
                    "A wrong id was passed. The 'entity_other' in this case must be the reification"
                    ", however the reification's id is not equal to the one from 'entity_other'"
                )
            triple_form_data["model_self_id"] = str(reification_instance.pk)
            triple = create_triple_by_form_data(triple_form_data)
            if triple is not None:
                related_triple_list.append(triple)
            
        return related_triple_list

    post_data = json.loads(request.body)
    try:
        reification_instance = process_reification_instance(post_data)
        related_triple_list_before = Triple.objects.filter(Q(subj=reification_instance) | Q(obj=reification_instance))
        related_triple_list_after = process_triples_to_reification(reification_instance, post_data["triple_data_to_reification_list"])
        related_triple_list_after += process_triples_from_reification(reification_instance, post_data["triple_data_from_reification_list"])
        for triple in related_triple_list_before:
            if triple not in related_triple_list_after:
                triple.delete()
    except FormException as e:
        response = JsonResponse(
            data={"error": str(e)},
            status=500,
            safe=False
        )
    else:
        response = JsonResponse(
            data={
                "form": render_reification_form(
                    model_self_class_str=post_data["model_self_class"],
                    reification_type_str=post_data["reification_type"],
                    model_self_id_str=post_data["model_self_id"],
                ),
                "table": render_reification_table(
                    request=request,
                    reification_type_str=post_data["reification_type"],
                    model_self_class_str=post_data["model_self_class"],
                    model_self_id_str=post_data["model_self_id"],
                    should_be_editable=True,
                )
            },
            status=200,
            safe=False
        )
    
    return response


def ajax_2_delete_reification(request):
    reification_class = caching.get_reification_class_of_name(request.POST["reification_type"])
    reification_class.objects.get(pk=request.POST["reification_id"]).delete()
    response = JsonResponse(
        data={
            "form": render_reification_form(
                model_self_class_str=request.POST["model_self_class"],
                reification_type_str=request.POST["reification_type"],
                model_self_id_str=request.POST["model_self_id"],
            ),
            "table": render_reification_table(
                request=request,
                reification_type_str=request.POST["reification_type"],
                model_self_class_str=request.POST["model_self_class"],
                model_self_id_str=request.POST["model_self_id"],
                should_be_editable=True,
            )
        },
        status=200,
        safe=False
    )
    
    return response