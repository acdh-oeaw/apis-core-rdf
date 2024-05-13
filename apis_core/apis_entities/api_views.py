from django.shortcuts import redirect
from rest_framework.views import APIView
from rest_framework.exceptions import NotFound

from apis_core.apis_metainfo.models import RootObject


class GetEntityGeneric(APIView):
    def get(self, request, pk):
        try:
            obj = RootObject.objects_inheritance.get_subclass(id=pk)
            return redirect(obj.get_api_detail_endpoint())
        except RootObject.DoesNotExist:
            raise NotFound
