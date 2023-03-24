import copy
import re

import yaml
from crispy_forms.bootstrap import Accordion, AccordionGroup
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout
from dal import autocomplete
from django import forms
from django.conf import settings
from django.contrib.contenttypes.models import ContentType
from django.core.exceptions import ValidationError
from django.db.models import Q
from django.urls import reverse

# import autocomplete_light.shortcuts as al
from django.utils.translation import ugettext_lazy as _
from apis_core.apis_relations.models import TempTriple, Property
from apis_core.apis_entities.fields import ListSelect2

# from apis_core.apis_entities.models import AbstractEntity
# from dal.autocomplete import ListSelect2
from apis_core.apis_entities.models import TempEntityClass
from apis_core.apis_metainfo.models import Text, Uri

# from apis_core.apis_relations.models import AbstractRelation
from apis_core.helper_functions import DateParser
from apis_core.helper_functions.RDFParser import RDFParser, APIS_RDF_URI_SETTINGS
from .tables import get_generic_relations_table, get_generic_triple_table
from apis_core.apis_entities.autocomplete3 import (
    PropertyAutocomplete,
    GenericEntitiesAutocomplete,
)

# from dal.autocomplete import ListSelect2

if "apis_highlighter" in settings.INSTALLED_APPS:
    from apis_highlighter.models import Annotation, AnnotationProject

# TODO RDF: Check if this should be removed or adapted
def validate_target_autocomplete(value):
    try:
        value = int(value)
    except ValueError:
        if value.startswith("http"):
            test = False
            sett = yaml.load(open(APIS_RDF_URI_SETTINGS, "r"))
            regx = [x["regex"] for x in sett["mappings"]]
            regx.append("http.*oeaw\.ac\.at")
            for k, v in getattr(settings, "APIS_AC_INSTANCES", {}).items():
                regx.append(v["url"].replace(".", "\."))
            for r in regx:
                if re.match(r, value):
                    test = True
            if not test:
                if Uri.objects.filter(uri=value).count() != 1:
                    raise ValidationError(
                        _(
                            "Invalid value: %(value)s, the url you are using is not configured"
                        ),
                        code="invalid",
                        params={"value": value},
                    )
        else:
            raise ValidationError(
                _("Invalid value: %(value)s, use either URLs or select a value"),
                code="invalid",
                params={"value": value},
            )


class GenericTripleForm(forms.ModelForm):
    # TODO RDF : Add Notes and references

    class Meta:
        model = TempTriple
        fields = [
            "subj",
            "obj",
            "prop",
            "start_date_written",
            "end_date_written",
        ]
        widgets = {
            "subj": forms.HiddenInput(),
            "obj": forms.HiddenInput(),
            "prop": forms.HiddenInput(),
        }

    def __init__(self, entity_type_self_str, entity_type_other_str):

        super().__init__()

        self.helper = FormHelper()
        self.helper.form_tag = False

        attrs = {
            "data-placeholder": "Type to get suggestions",
            "data-minimum-input-length": getattr(settings, "APIS_MIN_CHAR", 3),
            "data-html": True,
            "style": "width: 100%",
        }
        help_text_other_entity = (
            "Search and select or use an URL from a reference resource"
        )
        attrs_target = copy.deepcopy(attrs)
        attrs_target["data-tags"] = "1"

        # This assert only serves as a linking for us devs, to make explicit what internal object the class
        # Select2ListCreateChoiceField object afterwards uses.
        assert GenericEntitiesAutocomplete

        self.fields["other_entity"] = autocomplete.Select2ListCreateChoiceField(
            label="entity",
            widget=ListSelect2(
                url=reverse(
                    "apis:apis_entities:generic_entities_autocomplete",
                    kwargs={"entity": entity_type_other_str},
                ),
                attrs=attrs_target,
            ),
            help_text=help_text_other_entity,
        )

        # This assert only serves as a linking for us devs, to make explicit what internal object the class
        # Select2ListCreateChoiceField object afterwards uses.
        assert PropertyAutocomplete

        self.fields["property"] = autocomplete.Select2ListCreateChoiceField(
            label="property",
            widget=ListSelect2(
                url=reverse(
                    "apis:apis_relations:generic_property_autocomplete",
                    kwargs={
                        "entity_self": entity_type_self_str,
                        "entity_other": entity_type_other_str,
                    },
                ),
                attrs=attrs_target,
            ),
        )
        self.helper.include_media = False

    def load_subj_obj_prop(
        self,
        entity_instance_self,
        entity_instance_other,
        property_instance,
        property_direction,
    ):
        # the more important function here when writing data from an user input via an ajax call into this form.
        # Because here the direction of the property is respected. Hence the subject and object position of the
        # triple and the property name or name_reverse are loaded correctly here.

        if property_direction == PropertyAutocomplete.SELF_SUBJ_OTHER_OBJ_STR:

            triple_subj = entity_instance_self
            triple_obj = entity_instance_other
            property_direction_name = property_instance.name

        elif property_direction == PropertyAutocomplete.SELF_OBJ_OTHER_SUBJ_STR:

            triple_subj = entity_instance_other
            triple_obj = entity_instance_self
            property_direction_name = property_instance.name_reverse

        else:

            raise Exception("No valid property direction given.")

        self.fields["subj"].initial = triple_subj
        self.fields["obj"].initial = triple_obj
        self.fields["prop"].initial = property_instance

        property_initial_value = (
            f"id:{property_instance.pk}__direction:{property_direction}",
            property_direction_name,
        )
        self.fields["property"].initial = property_initial_value
        self.fields["property"].choices = [property_initial_value]

        other_entity_initial_value = (
            str(Uri.objects.get(root_object=entity_instance_other)),
            f"<span ><small>db</small> {str(entity_instance_other)}</span>",
        )
        self.fields["other_entity"].initial = other_entity_initial_value
        self.fields["other_entity"].choices = [other_entity_initial_value]

    def load_remaining_data_from_triple(self, triple):
        # Most data is loaded via the set_subj_obj function.
        # Here, load the rest from a pre-existing triple.
        #
        # This function is both used in get_form_ajax and save_form_ajax,
        # hence it's not feasible to assume existing user input as done
        # in 'load_remaining_data_from_input'

        self.fields["start_date_written"].initial = triple.start_date_written
        self.fields["end_date_written"].initial = triple.end_date_written
        self.instance = triple

    def load_remaining_data_from_input(
        self,
        start_date_written,
        end_date_written,
    ):
        # Most data is loaded via the set_subj_obj function.
        # Here, load the rest from the user input via the ajax post

        self.fields["start_date_written"].initial = start_date_written
        self.fields["end_date_written"].initial = end_date_written

    def save(self):
        if self.instance.pk is None:

            self.instance = TempTriple.objects.create(
                subj=self.fields["subj"].initial,
                obj=self.fields["obj"].initial,
                prop=self.fields["prop"].initial,
            )

        else:

            self.instance.subj = self.fields["subj"].initial
            self.instance.obj = self.fields["obj"].initial
            self.instance.prop = self.fields["prop"].initial

        self.instance.start_date_written = self.fields["start_date_written"].initial
        self.instance.end_date_written = self.fields["end_date_written"].initial
        self.instance.save()

        return self.instance

    def get_text_id(self):
        """
        Function to retrieve the highlighted text.
        :return: ID of text that was highlighted
        """
        return self.cleaned_data["HL_text_id"][5:]

    def get_html_table(self, entity_instance_self, entity_instance_other):
        table_class = get_generic_triple_table(
            other_entity_class_name=entity_instance_other.__class__.__name__.lower(),
            entity_pk_self=entity_instance_self.pk,
            detail=False,
        )

        table_object = table_class(
            data=TempTriple.objects.filter(
                (
                    Q(subj__self_contenttype=entity_instance_other.self_contenttype)
                    & Q(obj=entity_instance_self)
                )
                | (
                    Q(obj__self_contenttype=entity_instance_other.self_contenttype)
                    & Q(subj=entity_instance_self)
                )
            ),
            prefix=entity_instance_other.__class__.__name__,
        )

        return table_object
