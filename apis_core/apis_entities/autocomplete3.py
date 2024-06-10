#!/usr/bin/python
# -*- coding: utf-8 -*-
import json

from dal import autocomplete
from django import http
from django.contrib.contenttypes.models import ContentType

from apis_core.apis_entities.utils import get_entity_classes
from apis_core.apis_relations.models import Property


class PropertyAutocomplete(autocomplete.Select2ListView):
    # These constants are set so that they are defined in one place only and reused by fetching them elsewhere.
    SELF_SUBJ_OTHER_OBJ_STR = "self_subj_other_obj"
    SELF_OBJ_OTHER_SUBJ_STR = "self_obj_other_subj"

    def get_autocomplete_property_choices(self, self_model, other_model, search_str):
        contenttypes = [
            ContentType.objects.get_for_model(model) for model in get_entity_classes()
        ]
        self_contenttype = next(
            filter(lambda x: x.model == self_model.lower(), contenttypes)
        )
        other_contenttype = next(
            filter(lambda x: x.model == other_model.lower(), contenttypes)
        )

        rbc_self_subj_other_obj = Property.objects.filter(
            subj_class=self_contenttype,
            obj_class=other_contenttype,
            name_forward__icontains=search_str,
        )
        rbc_self_obj_other_subj = Property.objects.filter(
            subj_class=other_contenttype,
            obj_class=self_contenttype,
            name_reverse__icontains=search_str,
        )
        choices = []
        for rbc in rbc_self_subj_other_obj:
            choices.append(
                {
                    # misuse of the id item as explained above
                    "id": f"id:{rbc.pk}__direction:{self.SELF_SUBJ_OTHER_OBJ_STR}",
                    "text": rbc.name_forward,
                }
            )
        for rbc in rbc_self_obj_other_subj:
            choices.append(
                {
                    # misuse of the id item as explained above
                    "id": f"id:{rbc.pk}__direction:{self.SELF_OBJ_OTHER_SUBJ_STR}",
                    "text": rbc.name_reverse,
                }
            )
        return choices

    def get(self, request, *args, **kwargs):
        more = False
        choices = self.get_autocomplete_property_choices(
            kwargs["entity_self"], kwargs["entity_other"], self.q
        )
        return http.HttpResponse(
            json.dumps(
                {"results": choices, "pagination": {"more": more}, "abcde": "0"}
            ),
            content_type="application/json",
        )
