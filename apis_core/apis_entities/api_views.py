import re

from django.shortcuts import redirect
from rest_framework.pagination import PageNumberPagination
from rest_framework.parsers import FileUploadParser
from rest_framework.response import Response
from rest_framework.reverse import reverse_lazy
from rest_framework.views import APIView
from rest_framework.exceptions import NotFound

from apis_core.apis_metainfo.models import Uri, RootObject
from apis_core.utils import caching


class StandardResultsSetPagination(PageNumberPagination):
    page_size = 25
    page_size_query_param = "page_size"
    max_page_size = 1000


class GetEntityGeneric(APIView):
    def get(self, request, pk):
        try:
            obj = RootObject.objects_inheritance.get_subclass(id=pk)
            return redirect(obj.get_api_detail_endpoint())
        except RootObject.DoesNotExist:
            raise NotFound


class ResolveAbbreviations(APIView):
    parser_classes = (FileUploadParser,)

    def put(self, request, filename, format=None):
        return Response(status=204)


class GetOrCreateEntity(APIView):
    def get(self, request):
        entity = request.query_params.get("entity2", None)
        uri = request.query_params.get("uri", None)
        if uri and uri.startswith(("http:", "https:")):
            u, _ = Uri.objects.get_or_create(uri=uri)
            ent = u.root_object
        else:
            r1 = re.search(r"^[^<]+", uri)
            r2 = re.search(r"<([^>]+)>", uri)
            q_d = dict()
            q_d["name"] = r1
            if r2:
                for x in r2.group(1).split(";"):
                    x2 = x.split("=")
                    q_d[x2[0].strip()] = x2[1].strip()
            if entity == "person":
                r1_2 = r1.group(0).split(",")
                if len(r1_2) == 2:
                    q_d["first_name"] = r1_2[1].strip()
                    q_d["name"] = r1_2[0].strip()
            ent = caching.get_ontology_class_of_name(entity).objects.create(**q_d)
        res = {
            "id": ent.pk,
            "url": reverse_lazy(
                "apis:apis_entities:generic_entities_edit_view",
                request=request,
                kwargs={"pk": ent.pk, "entity": entity},
            ),
        }
        return Response(res)
