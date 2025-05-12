from django.db.models import Q
from django.shortcuts import redirect
from drf_spectacular.utils import extend_schema, inline_serializer
from rest_framework.exceptions import NotFound
from rest_framework.generics import ListAPIView
from rest_framework.permissions import AllowAny
from rest_framework.views import APIView

from apis_core.apis_entities.serializers import MinimalEntitySerializer
from apis_core.apis_entities.utils import get_entity_classes
from apis_core.apis_metainfo.models import RootObject
from apis_core.utils.filters import CustomSearchFilter


class GetEntityGeneric(APIView):
    permission_classes = [AllowAny]

    @extend_schema(
        responses=inline_serializer(name="GetEntityGenericSerializer", fields={})
    )
    def get(self, request, pk):
        try:
            obj = RootObject.objects_inheritance.get_subclass(id=pk)
            return redirect(obj.get_api_detail_endpoint())
        except RootObject.DoesNotExist:
            raise NotFound


class ListEntityGeneric(ListAPIView):
    serializer_class = MinimalEntitySerializer
    filter_backends = [CustomSearchFilter]

    def get_queryset(self):
        entities = get_entity_classes()
        entities = [entity._meta.model_name for entity in entities]
        q = Q()
        for entity in entities:
            q |= Q(**{f"{entity}__isnull": False})
        return RootObject.objects_inheritance.select_subclasses().filter(q)
