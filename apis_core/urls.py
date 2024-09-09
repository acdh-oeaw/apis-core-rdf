from django.conf import settings
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


if "apis_core.apis_metainfo" in settings.INSTALLED_APPS:
    from apis_core.apis_metainfo.urls import router as apis_metainfo_router

    router.registry.extend(apis_metainfo_router.registry)


if "apis_core.apis_entities" in settings.INSTALLED_APPS:
    urlpatterns.append(path("entities/", include("apis_core.apis_entities.urls")))
    from apis_core.apis_entities.urls import api_routes

    urlpatterns.append(path("api/", include(api_routes)))


if "apis_core.apis_relations" in settings.INSTALLED_APPS:
    urlpatterns.append(path("relations/", include("apis_core.apis_relations.urls")))


if "apis_core.relations" in settings.INSTALLED_APPS:
    urlpatterns.append(path("relations/", include("apis_core.relations.urls")))


if "apis_core.history" in settings.INSTALLED_APPS:
    urlpatterns.append(path("history/", include("apis_core.history.urls")))


if "apis_core.collections" in settings.INSTALLED_APPS:
    urlpatterns.append(path("collections/", include("apis_core.collections.urls")))


if "apis_core.documentation" in settings.INSTALLED_APPS:
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
