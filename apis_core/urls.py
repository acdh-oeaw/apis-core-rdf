"""
Main entry point for APIS routes
"""

from django.apps import apps
from django.contrib import admin
from django.urls import include, path
from drf_spectacular.views import (
    SpectacularAPIView,
    SpectacularRedocView,
    SpectacularSwaggerView,
)

from apis_core.generic.routers import CustomDefaultRouter

app_name = "apis_core"

urlpatterns = [
    path("", include("apis_core.core.urls")),
    path("", include("apis_core.generic.urls")),
    path("admin/", admin.site.urls),
    path("accounts/", include("django.contrib.auth.urls")),
]

router = CustomDefaultRouter()


if apps.is_installed("apis_core.search"):
    urlpatterns.append(path("", include("apis_core.search.urls")))


if apps.is_installed("apis_core.entities"):
    urlpatterns.append(path("", include("apis_core.entities.urls")))


if apps.is_installed("apis_core.uri"):
    from apis_core.uri.urls import router as apis_uris_router

    router.registry.extend(apis_uris_router.registry)


if apps.is_installed("apis_core.apis_entities"):
    urlpatterns.append(path("entities/", include("apis_core.apis_entities.urls")))
    from apis_core.apis_entities.urls import api_routes

    urlpatterns.append(path("api/", include(api_routes)))


if apps.is_installed("apis_core.relations"):
    urlpatterns.append(path("relations/", include("apis_core.relations.urls")))


if apps.is_installed("apis_core.history"):
    urlpatterns.append(path("history/", include("apis_core.history.urls")))


if apps.is_installed("apis_core.collections"):
    urlpatterns.append(path("collections/", include("apis_core.collections.urls")))


if apps.is_installed("apis_core.documentation"):
    urlpatterns.append(path("", include("apis_core.documentation.urls")))


urlpatterns.append(path("api/", include(router.urls)))
urlpatterns.append(path("api-auth/", include("rest_framework.urls")))


urlpatterns.append(path("swagger/schema/", SpectacularAPIView.as_view(), name="schema"))
urlpatterns.append(
    path(
        "swagger/schema/swagger-ui/",
        SpectacularSwaggerView.as_view(url_name="apis_core:schema"),
        name="swagger-ui",
    )
)
urlpatterns.append(
    path(
        "swagger/schema/redoc/",
        SpectacularRedocView.as_view(url_name="apis_core:schema"),
        name="redoc",
    )
)
