from django.http import JsonResponse
from django.views import View
from apis_core import __version__ as version


class ApisVersion(View):
    def get(self, request, *args, **kwargs):
        return JsonResponse({"version": version})
