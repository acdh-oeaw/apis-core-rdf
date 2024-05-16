#!/usr/bin/python
# -*- coding: utf-8 -*-
import json
import operator
from functools import reduce

from dal import autocomplete
from django import http
from django.contrib.contenttypes.models import ContentType
from django.core.exceptions import FieldError
from django.db.models import Q

from apis_core.utils.caching import get_autocomplete_property_choices
from apis_core.utils.settings import get_entity_settings_by_modelname


# TODO RDF: Check if this should be removed or adapted
class GenericNetworkEntitiesAutocomplete(autocomplete.Select2ListView):
    def get(self, request, *args, **kwargs):
        entity = self.kwargs["entity"]
        q = self.q
        if q.startswith("reg:"):
            results = []
            if entity.lower() == "person":
                filen = "reg_persons.json"
            elif entity.lower() == "place":
                filen = "reg_places.json"
            with open(filen, "r") as reg:
                r1 = json.load(reg)
                r_dict = dict()
                for r2 in r1:
                    if q[4:].lower() in r2[1].lower():
                        if r2[1] in r_dict.keys():
                            r_dict[r2[1]] += "|{}".format(r2[0])
                        else:
                            r_dict[r2[1]] = r2[0]
            for k in r_dict.keys():
                results.append({"id": "reg:" + r_dict[k], "text": k})

        else:
            ent_model = ContentType.objects.get(
                app_label__startswith="apis_", model=entity
            ).model_class()
            try:
                arg_list = [
                    Q(**{x + "__icontains": q})
                    for x in get_entity_settings_by_modelname(entity.title()).get(
                        "search", []
                    )
                ]
            except KeyError:
                arg_list = [Q(**{x + "__icontains": q}) for x in ["name"]]
            try:
                res = ent_model.objects.filter(
                    reduce(operator.or_, arg_list)
                ).distinct()
            except FieldError:
                arg_list = [Q(**{x + "__icontains": q}) for x in ["text"]]
                res = ent_model.objects.filter(
                    reduce(operator.or_, arg_list)
                ).distinct()
            results = [{"id": x.pk, "text": str(x)} for x in res]
        return http.HttpResponse(
            json.dumps({"results": results}), content_type="application/json"
        )


class PropertyAutocomplete(autocomplete.Select2ListView):
    # These constants are set so that they are defined in one place only and reused by fetching them elsewhere.
    SELF_SUBJ_OTHER_OBJ_STR = "self_subj_other_obj"
    SELF_OBJ_OTHER_SUBJ_STR = "self_obj_other_subj"

    def get(self, request, *args, **kwargs):
        more = False
        choices = get_autocomplete_property_choices(
            kwargs["entity_self"], kwargs["entity_other"], self.q
        )
        return http.HttpResponse(
            json.dumps(
                {"results": choices, "pagination": {"more": more}, "abcde": "0"}
            ),
            content_type="application/json",
        )
