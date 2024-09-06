import json

from django.contrib.auth.decorators import login_required
from django.contrib.contenttypes.models import ContentType
from django.http import HttpResponse
from django.template.loader import render_to_string

from apis_core.apis_entities.autocomplete3 import PropertyAutocomplete
from apis_core.apis_entities.utils import get_entity_classes
from apis_core.apis_relations.forms import GenericTripleForm
from apis_core.apis_relations.models import Property, TempTriple, Triple
from apis_core.generic.views import List


class GenericRelationView(List):
    def setup(self, *args, **kwargs):
        super().setup(*args, **kwargs)
        if self.kwargs["entity"] == "property":
            self.model = Property
        else:
            self.model = Triple
        self.queryset = self.model.objects.all()


# TODO RDF: After full conversion to ne ajax logic, remove this function
@login_required
def get_form_ajax(request):
    """Returns forms rendered in html"""

    form_name = request.POST.get("FormName")
    SiteID = int(request.POST.get("SiteID"))
    ButtonText = request.POST.get("ButtonText")
    ObjectID = request.POST.get("ObjectID")
    entity_type_self_str = request.POST.get("entity_type")

    if ObjectID is None and form_name.startswith("triple_form_"):
        # If this is the case, then instantiate an empty form

        entity_type_other_str = form_name.split("_to_")[1]

        form = GenericTripleForm(
            entity_type_self_str=entity_type_self_str,
            entity_type_other_str=entity_type_other_str,
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

        entity_type_other_str = entity_instance_other.__class__.__name__
        entity_type_self_str = entity_instance_self.__class__.__name__
        form_name = f"triple_form_{entity_type_self_str.lower()}_to_{entity_type_other_str.lower()}"

        form = GenericTripleForm(
            entity_type_self_str=entity_type_self_str,
            entity_type_other_str=entity_type_other_str,
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

    param_dict = {
        "entity_type": entity_type_self_str,
        "form": form,
        "type1": form_name,
        "url2": "save_ajax_" + form_name,
        "button_text": ButtonText,
        "ObjectID": ObjectID,
        "SiteID": SiteID,
    }

    rendered_form_str = render_to_string(
        "apis_relations/_ajax_form.html",  # rel_form_logic_breadcrumb (for refinding the implicit connections)
        context=param_dict,
    )

    data = {"tab": form_name, "form": rendered_form_str}

    return HttpResponse(json.dumps(data), content_type="application/json")


# TODO RDF: Re-implement highlighter and label form
@login_required
def save_ajax_form(
    request, entity_type, kind_form, SiteID, ObjectID=False
):  # rel_form_logic_breadcrumb (for refinding the implicit connections)
    """Tests validity and saves AjaxForms, returns them when validity test fails"""

    self_other = kind_form.split("triple_form_")[1].split("_to_")
    entity_type_self_str = self_other[0]
    entity_type_other_str = self_other[1]
    contenttypes = [
        ContentType.objects.get_for_model(model) for model in get_entity_classes()
    ]
    entity_type_self_class = next(
        filter(lambda x: x.model == entity_type_self_str.lower(), contenttypes)
    ).model_class()
    entity_type_other_class = next(
        filter(lambda x: x.model == entity_type_other_str.lower(), contenttypes)
    ).model_class()
    entity_instance_self = entity_type_self_class.objects.get(pk=SiteID)
    entity_instance_other = entity_type_other_class.get_or_create_uri(
        uri=request.POST["other_entity"]
    )
    start_date_written = request.POST["start_date_written"]
    end_date_written = request.POST["end_date_written"]
    property_param_dict = {}
    for param_pair in request.POST["property"].split("__"):
        param_pair_split = param_pair.split(":")
        property_param_dict[param_pair_split[0]] = param_pair_split[1]
    property_instance = Property.objects.get(pk=property_param_dict["id"])
    property_direction = property_param_dict["direction"]

    form = GenericTripleForm(entity_type_self_str, entity_type_other_str)
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
    form.fields["notes"].initial = request.POST["notes"]
    form.save()

    data = {
        "test": True,
        "tab": kind_form,
        "call_function": "EntityRelationForm_response",
        "instance": form.instance.get_web_object(),
        "table_html": form.get_html_table(
            entity_instance_self, entity_instance_other, request
        ).as_html(request),
        "text": None,
        "right_card": True,
    }
    return HttpResponse(json.dumps(data), content_type="application/json")
