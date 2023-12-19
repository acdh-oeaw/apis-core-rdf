import json

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated

from apis_core.utils.helpers import datadump_serializer


class Dumpdata(APIView):
    """
    provide an API endpoint that outputs the datadump of an APIS installation

    this is a bit of a hack, becaus we first use the Django JSON serializer to
    serialize the data using natural keys, then we use json.loads to so we can
    output it as an API reponse.
    so basically: serialize -> deserialize -> serialize
    """

    permission_classes = [IsAuthenticated]

    def get(self, request, *args, **kwargs):
        params = request.query_params.dict()
        app_labels = params.pop("app_labels", [])
        if app_labels:
            app_labels = app_labels.split(",")
        return Response(json.loads(datadump_serializer(app_labels, "json")))
