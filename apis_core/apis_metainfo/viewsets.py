from django.http import HttpResponseRedirect, QueryDict
from django.shortcuts import get_object_or_404
from drf_spectacular.utils import OpenApiParameter, OpenApiTypes, extend_schema
from rest_framework import viewsets
from rest_framework.response import Response

from apis_core.apis_metainfo.models import Uri


class UriToObjectViewSet(viewsets.ViewSet):
    """
    This API route provides an endpoint for resolving URIs and forwarding
    them to the endpoint in the local instance. Pass a `uri` request
    parameter to resolve the uri.
    """

    @extend_schema(
        parameters=[
            OpenApiParameter(
                "uri", OpenApiTypes.URI, OpenApiParameter.QUERY
            ),  # path variable was overridden
        ],
        responses={301: None},
        description="This API route provides an endpoint for resolving URIs and forwarding them to the endpoint in the local instance. Pass a `uri` request parameter to resolve the uri.",
    )
    def list(self, request):
        params = request.query_params.dict()
        uri = params.pop("uri", None)
        if uri:
            u = get_object_or_404(Uri, uri=request.query_params.get("uri"))
            r = u.content_object.get_api_detail_endpoint()
            if params:
                r += "?" + QueryDict.from_keys(params).urlencode()
            return HttpResponseRedirect(r)
        return Response()
