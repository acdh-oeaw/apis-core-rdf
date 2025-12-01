from django.http import HttpResponse
from django.shortcuts import redirect
from django.views.generic.base import View
from django.views.generic.detail import SingleObjectMixin

from apis_core.entities.models import EntityID


class CanonicalEntity(View, SingleObjectMixin):
    model = EntityID
    accepted_media_types = ["text/html", "application/json"]

    def get(self, request, *args, **kwargs):
        match request.get_preferred_type(self.accepted_media_types):
            case "text/html":
                return redirect(self.get_object().content_object.get_absolute_url())
            case "application/json":
                return redirect(
                    self.get_object().content_object.get_api_detail_endpoint()
                )
            case _:
                return HttpResponse(
                    status_code=406,
                    headers={"Accept": ",".join(self.accepted_media_types)},
                )
