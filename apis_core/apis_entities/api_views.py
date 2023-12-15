import re
from io import TextIOWrapper

from django.conf import settings
from django.http import Http404
from rest_framework.generics import GenericAPIView
from rest_framework.pagination import PageNumberPagination
from rest_framework.parsers import FileUploadParser
from rest_framework.response import Response
from rest_framework.reverse import reverse_lazy
from rest_framework.settings import api_settings
from rest_framework.views import APIView

from apis_core.apis_metainfo.models import Uri, RootObject
from .api_renderers import (
    EntityToTEI,
    EntityToCIDOCXML,
    EntityToCIDOCN3,
    EntityToCIDOCNQUADS,
    EntityToCIDOCTURTLE,
)
from .serializers_generic import EntitySerializer
from apis_core.utils import caching
from apis_core.utils.utils import get_python_safe_module_path


class StandardResultsSetPagination(PageNumberPagination):
    page_size = 25
    page_size_query_param = "page_size"
    max_page_size = 1000


class GetEntityGeneric(GenericAPIView):
    serializer_class = EntitySerializer
    queryset = RootObject.objects.all()
    renderer_classes = tuple(api_settings.DEFAULT_RENDERER_CLASSES) + (
        EntityToTEI,
        EntityToCIDOCXML,
        EntityToCIDOCN3,
        EntityToCIDOCNQUADS,
        EntityToCIDOCTURTLE,
    )
    if getattr(settings, "APIS_RENDERERS", None) is not None:
        rend_add = tuple()
        for rd in settings.APIS_RENDERERS:
            rend_mod = __import__(rd)
            for name, cls in rend_mod.__dict__.items():
                rend_add + (cls,)
        renderer_classes += rend_add

    def get_object(self, pk, request):
        try:
            return RootObject.objects_inheritance.get_subclass(pk=pk)
        except RootObject.DoesNotExist:
            uri2 = Uri.objects.filter(uri=request.build_absolute_uri())
            if uri2.count() == 1:
                return RootObject.objects_inheritance.get_subclass(pk=uri2[0].entity_id)
            else:
                raise Http404

    def get(self, request, pk):
        ent = self.get_object(pk, request)
        # we let users override the default serializer based on the chosen renderer
        # the name of the method has to be the full path of the renderer, dots
        # replaced with underscores
        # i.e.: apis_core_apis_entities_api_renderers_EntityToTEI
        renderer_full_path = get_python_safe_module_path(self.request.accepted_renderer)
        if hasattr(ent, renderer_full_path):
            res = getattr(ent, renderer_full_path)(ent, context={"request": request})
        else:
            res = EntitySerializer(ent, context={"request": request})
        return Response(res.data)


class ResolveAbbreviations(APIView):
    parser_classes = (FileUploadParser,)

    def put(self, request, filename, format=None):
        file_obj = request.data["file"]
        txt = TextIOWrapper(file_obj, encoding="utf8")
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
