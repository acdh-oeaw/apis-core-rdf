from rest_framework.routers import DefaultRouter

from apis_core.apis_metainfo.viewsets import UriToObjectViewSet

router = DefaultRouter()

router.register(r"metainfo/uritoobject", UriToObjectViewSet, basename="uritoobject")
