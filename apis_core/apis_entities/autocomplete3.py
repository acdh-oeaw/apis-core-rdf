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


class CustomEntityAutocompletes(object):
    """A class for collecting all the custom autocomplete functions for one entity.

    Attributes:

    - self.entity: (string) entity types
    - self.more: (boolean) if more results can be fetched (pagination)
    - self.page_size: (integer) page size
    - self.results: (list) results
    - self.query: (string) query string

    Methods:
    - self.more(): fetch more results
    """

    def __init__(self, entity, query, page_size=20, offset=0, *args, **kwargs):
        """
        :param entity: (string) entity type to fetch additional autocompletes for
        """
        func_list = {}
        if entity not in func_list.keys():
            self.results = None
            return None
        res = []
        more = dict()
        more_gen = False
        for x in func_list[entity]:
            res2 = x().query(query, page_size, offset)
            if len(res2) == page_size:
                more[x.__name__] = (True, offset + 1)
                more_gen = True
            res.extend(res2)
        self.results = res
        self.page_size = page_size
        self.more = more_gen
        self._more_dict = more
        self.query = query
        self.offset = offset

    def get_more(self):
        """
        Function to retrieve more results.
        """
        res4 = []
        for key, value in self._more_dict.items():
            if value[0]:
                res3 = globals()[key](self.query, self.page_size, value[1])
                if len(res3) == self.page_size:
                    self._more_dict[key] = (True, value[1] + 1)
                else:
                    self._more_dict[key] = (False, value[1])
                self.results.extend(res3)
                res4.extend(res3)
        return res4


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
