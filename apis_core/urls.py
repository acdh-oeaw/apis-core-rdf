from django.conf import settings
from django.contrib import admin
from django.contrib.auth.decorators import login_required
from django.urls import include, path, re_path
from django.views.generic import TemplateView
from django.views.static import serve
from drf_spectacular.views import (
    SpectacularAPIView,
    SpectacularRedocView,
    SpectacularSwaggerView,
)

from apis_core.apis_entities.api_views import GetEntityGeneric, ListEntityGeneric
from apis_core.apis_metainfo.viewsets import UriToObjectViewSet
from apis_core.core.views import Dumpdata
from apis_core.generic.routers import CustomDefaultRouter

app_name = "apis_core"

router = CustomDefaultRouter()
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
    path("api/entities/", ListEntityGeneric.as_view()),
    path("api/dumpdata", Dumpdata.as_view()),
    path("", include("apis_core.generic.urls", namespace="generic")),
]
if "apis_core.history" in settings.INSTALLED_APPS:
    urlpatterns.append(
        path("history/", include("apis_core.history.urls", namespace="history"))
    )

if "apis_core.relations" in settings.INSTALLED_APPS:
    urlpatterns.append(path("relations/", include("apis_core.relations.urls")))

if "apis_core.collections" in settings.INSTALLED_APPS:
    urlpatterns.append(path("collections/", include("apis_core.collections.urls")))

if "apis_core.documentation" in settings.INSTALLED_APPS:
    urlpatterns.append(path("", include("apis_core.documentation.urls")))
