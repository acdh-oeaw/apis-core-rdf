import json

from django.contrib import messages
from django.contrib.auth import views as auth_views
from django.urls import reverse_lazy
from django.utils.translation import gettext_lazy as _
from drf_spectacular.utils import OpenApiParameter, extend_schema, inline_serializer
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

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

    @extend_schema(
        parameters=[OpenApiParameter(name="app_labels", type=str, many=True)],
        responses={200: inline_serializer(name="DumpDataResponse", fields={})},
    )
    def get(self, request, *args, **kwargs):
        params = request.query_params.dict()
        app_labels = params.pop("app_labels", [])
        if app_labels:
            app_labels = app_labels.split(",")
        return Response(json.loads(datadump_serializer(app_labels, "json")))


class PasswordChangeView(auth_views.PasswordChangeView):
    template_name = "profile/password-change.html"
    success_url = reverse_lazy("apis_core:password-change")

    def form_valid(self, form):
        ret = super().form_valid(form)
        messages.success(
            self.request,
            _("Password for %(user)s changed.").format(user=self.request.user),
        )
        return ret
