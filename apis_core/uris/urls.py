from django.urls import re_path
from rest_framework.routers import DefaultRouter

from apis_core.uris.views import UriCreateView
from apis_core.uris.viewsets import UriToObjectViewSet

router = DefaultRouter()

router.register(r"metainfo/uritoobject", UriToObjectViewSet, basename="uritoobject")

urlpatterns = [
    re_path(
        r"uris.uri/create/(?P<app_label>[^\.]+).(?P<model>[^\.]+)/(?P<pk>\d+)",
        UriCreateView.as_view(),
        name="createuri",
    )
]
