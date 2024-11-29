import copy

from crispy_forms.helper import FormHelper
from dal import autocomplete
from django import forms
from django.conf import settings
from django.contrib.contenttypes.models import ContentType
from django.db.models import Q
from django.urls import reverse
from django_tables2 import RequestConfig

from apis_core.apis_entities.autocomplete3 import (
    PropertyAutocomplete,
)
from apis_core.apis_entities.fields import ListSelect2
from apis_core.apis_entities.utils import get_entity_classes
from apis_core.apis_metainfo.models import Uri
from apis_core.apis_relations.models import TempTriple
from apis_core.utils.settings import get_entity_settings_by_modelname

from .tables import get_generic_triple_table


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
            "notes",
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

        contenttypes = [
            ContentType.objects.get_for_model(model) for model in get_entity_classes()
        ]
        ct = next(
            filter(lambda x: x.model == entity_type_other_str.lower(), contenttypes)
        )
        url = reverse("apis_core:generic:autocomplete", args=[ct]) + "?create=True"

        self.fields["other_entity"] = autocomplete.Select2ListCreateChoiceField(
            label="entity",
            widget=ListSelect2(
                url=url,
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
                    "apis_core:apis_relations:generic_property_autocomplete",
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
        # triple and the property name_forward or name_reverse are loaded correctly here.

        if property_direction == PropertyAutocomplete.SELF_SUBJ_OTHER_OBJ_STR:
            triple_subj = entity_instance_self
            triple_obj = entity_instance_other
            property_direction_name = property_instance.name_forward

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

        content_type = ContentType.objects.get_for_model(entity_instance_other)
        other_entity_initial_value = (
            str(
                Uri.objects.filter(
                    content_type=content_type, object_id=entity_instance_other.id
                ).first()
            ),
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
        self.fields["notes"].initial = triple.notes
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
        self.instance.notes = self.fields["notes"].initial
        self.instance.save()

        return self.instance

    def get_text_id(self):
        """
        Function to retrieve the highlighted text.
        :return: ID of text that was highlighted
        """
        return self.cleaned_data["HL_text_id"][5:]

    def get_html_table(self, entity_instance_self, entity_instance_other, request):
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
            request=request,
        )
        entity_settings = get_entity_settings_by_modelname(
            entity_instance_self.__class__.__name__
        )
        per_page = entity_settings.get("relations_per_page", 10)
        RequestConfig(request, paginate={"per_page": per_page}).configure(table_object)

        return table_object
