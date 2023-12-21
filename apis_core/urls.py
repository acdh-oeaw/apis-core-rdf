from django.urls import include, re_path
from django.contrib import admin
from django.contrib.auth.decorators import login_required
from django.urls import path
from django.views.static import serve
from django.views.generic import TemplateView
from rest_framework import routers

from apis_core.api_routers import views

# from apis_core.apis_entities.api_views import (
#     NetJsonViewSet,
#     PlaceGeoJsonViewSet,
# )
from apis_core.utils import caching
from apis_core.apis_metainfo.viewsets import UriToObjectViewSet
from apis_core.core.views import Dumpdata
from apis_core.apis_entities.api_views import GetEntityGeneric

from drf_spectacular.views import (
    SpectacularAPIView,
    SpectacularSwaggerView,
    SpectacularRedocView,
)

app_name = "apis_core"

router = routers.DefaultRouter()
for app_label, model_str in caching.get_all_class_modules_and_names():
    if "_" in app_label:
        route_prefix = app_label.split("_")[1]
    else:
        route_prefix = app_label
    try:
        router.register(
            r"{}/{}".format(route_prefix, model_str.lower()),
            views[model_str.lower()],
            model_str.lower(),
        )
    except Exception:
        print("{} not found, skipping".format(model_str.lower()))

# inject the manually created UriToObjectViewSet into the api router
router.register(r"metainfo/uritoobject", UriToObjectViewSet, basename="uritoobject")


urlpatterns = [
    path("", TemplateView.as_view(template_name="base.html"), name="apis_index"),
    path("admin/", admin.site.urls),
    path("swagger/schema/", SpectacularAPIView.as_view(), name="schema"),
    # Optional UI:
    path(
        "swagger/schema/swagger-ui/",
        SpectacularSwaggerView.as_view(url_name="apis_core:schema"),
        name="swagger-ui",
    ),
    path(
        "swagger/schema/redoc/",
        SpectacularRedocView.as_view(url_name="apis_core:schema"),
        name="redoc",
    ),
    path(
        "entities/", include("apis_core.apis_entities.urls", namespace="apis_entities")
    ),
    path(
        "relations/",
        include("apis_core.apis_relations.urls", namespace="apis_relations"),
    ),
    path(
        "metainfo/",
        include("apis_core.apis_metainfo.urls", namespace="apis_metainfo"),
    ),
    path(
        "api/", include((router.urls, "apis_core"), namespace="apis_api")
    ),  # routers do not support namespaces out of the box
    path("api-auth/", include("rest_framework.urls", namespace="rest_framework")),
    re_path(
        r"^docs/(?P<path>.*)$",
        login_required(serve),
        {"document_root": "apis-core/docs/_build/html"},
        "docs",
    ),
    path("accounts/", include("django.contrib.auth.urls")),
    path(
        "entity/<int:pk>/",
        GetEntityGeneric.as_view(),
        name="GetEntityGeneric",
    ),
    path("api/dumpdata", Dumpdata.as_view()),
    path("", include("apis_core.generic.urls", namespace="generic")),
]
