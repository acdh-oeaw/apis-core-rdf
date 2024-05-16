from django.shortcuts import redirect
from django.db.models import Q
from rest_framework.views import APIView
from rest_framework.exceptions import NotFound
from rest_framework.generics import ListAPIView

from apis_core.apis_metainfo.models import RootObject
from apis_core.apis_entities.serializers import MinimalEntitySerializer
from apis_core.apis_entities.utils import get_entity_classes


class GetEntityGeneric(APIView):
    def get(self, request, pk):
        try:
            obj = RootObject.objects_inheritance.get_subclass(id=pk)
            return redirect(obj.get_api_detail_endpoint())
        except RootObject.DoesNotExist:
            raise NotFound


class ListEntityGeneric(ListAPIView):
    serializer_class = MinimalEntitySerializer

    def get_queryset(self):
        entities = get_entity_classes()
        entities = [entity._meta.model_name for entity in entities]
        q = Q()
        for entity in entities:
            q |= Q(**{f"{entity}__isnull": False})
        return RootObject.objects_inheritance.select_subclasses().filter(q)
