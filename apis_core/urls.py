from django.conf import settings
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
# from apis_core.apis_vocabularies.api_views import UserViewSet
from apis_core.utils import helpers
from apis_core.apis_metainfo.viewsets import UriToObjectViewSet
from apis_core.core.views import Dumpdata

app_name = "apis_core"

router = routers.DefaultRouter()
for model in helpers.get_apis_model_classes() + helpers.get_entities_model_classes():
    app_label, modelname = model._meta.label_lower.split(".")
    if "_" in app_label:
        route_prefix = app_label.split("_")[1]
    else:
        route_prefix = app_label
    try:
        router.register(
            r"{}/{}".format(route_prefix, modelname),
            views[modelname],
            modelname,
        )
    except Exception:
        print("{} not found, skipping".format(modelname))

# inject the manually created UriToObjectViewSet into the api router
router.register(r"metainfo/uritoobject", UriToObjectViewSet, basename="uritoobject")

# router.register(r"users", UserViewSet)
# router.register(r"GeoJsonPlace", PlaceGeoJsonViewSet, "PlaceGeoJson")
# router.register(r"NetJson", NetJsonViewSet, "NetJson")


# from drf_yasg.views import get_schema_view as get_schema_view2
# from drf_yasg import openapi
from drf_spectacular.views import (
    SpectacularAPIView,
    SpectacularSwaggerView,
    SpectacularRedocView,
)


# schema_view2 = get_schema_view2(
#   openapi.Info(
#      title="APIS API",
#      default_version='v1',
#      description="Hyperlinked API of the APIS Framework",
# terms_of_service="https://www.google.com/policies/terms/",
#      contact=openapi.Contact(email="matthias.schloegl@oeaw.ac.at"),
#      license=openapi.License(name="MIT"),
#   ),
#   public=True,
#   permission_classes=(permissions.AllowAny,),
# )

# class APISSchemaGenerator(OpenAPISchemaGenerator):
#    info = "APIS test"
#    title = "APIS_API v2"

#    def __init__(self, *args, **kwargs):
#        super(APISSchemaGenerator, self).__init__(*args, **kwargs)


# class SchemaViewSwagger(schema_view2):
#    generator_class = APISSchemaGenerator

#    def get_filter_parameters(self, filter_backend):
#       if isinstance(filter_backend, DjangoFilterBackend):
#            result = super(SchemaViewSwagger, self).get_filter_parameters(filter_backend)
#            for param in result:
#                if not param.get('description', ''):
#                    param.description = "Filter the returned list by {field_name}".format(field_name=param.name)

#            return result

#        return NotHandled

#    def get_operation(self, operation_keys):
#        super(SchemaViewSwagger, self).get_operation(operation_keys)

#    def __init__(self, *args, **kwargs):
#        super(SchemaViewSwagger, self).__init__(*args, **kwargs)


def build_apis_mock_request(method, path, view, original_request, **kwargs):
    # default mock request
    request = build_mock_request(method, path, view, original_request, **kwargs)
    # the added wagtail magic
    request.router = router
    return request


from apis_core.apis_entities.api_views import GetEntityGeneric

urlpatterns = [
    path("", TemplateView.as_view(template_name="base.html"), name="apis_index"),
    path("admin/", admin.site.urls),
    # url(r'^swagger(?P<format>\.json|\.yaml)$', SchemaViewSwagger.without_ui(cache_timeout=-1), name='schema-json'),
    # url(r'^swagger/$', SchemaViewSwagger.with_ui('swagger', cache_timeout=-1), name='schema-swagger-ui'),
    # url(r'^redoc/$', SchemaViewSwagger.with_ui('redoc', cache_timeout=-1), name='schema-redoc'),
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
    path("labels/", include("apis_core.apis_labels.urls", namespace="apis_labels")),
    path(
        "entities/", include("apis_core.apis_entities.urls", namespace="apis_entities")
    ),
    path(
        "relations/",
        include("apis_core.apis_relations.urls", namespace="apis_relations"),
    ),
    path(
        "vocabularies/",
        include("apis_core.apis_vocabularies.urls", namespace="apis_vocabularies"),
    ),
    path(
        "metainfo/",
        include("apis_core.apis_metainfo.urls", namespace="apis_metainfo"),
    ),
    path(
        "metainfo-ac/",
        include("apis_core.apis_metainfo.dal_urls", namespace="apis_metainfo-ac"),
    ),
    # url(r'^autocomplete/', include('autocomplete_light.urls')),
    path(
        "api/", include((router.urls, "apis_core"), namespace="apis_api")
    ),  # routers do not support namespaces out of the box
    # path('openapi-2', schema_view),
    # path('openapi-api', get_schema_view(
    #    title="APIS",
    #    description="APIS API schema definition",
    #    urlconf='apis_core.apis_entities.api_urls',
    # ), name='openapi-schema-api'),
    path("api-auth/", include("rest_framework.urls", namespace="rest_framework")),
    # url(r'^api-schema/', schema_view),
    re_path(
        r"^docs/(?P<path>.*)$",
        login_required(serve),
        {"document_root": "apis-core/docs/_build/html"},
        "docs",
    ),
    # url(r'^docs/', include('sphinxdoc.urls')),
    # url(r'^accounts/', include('registration.backends.simple.urls')),
    path("accounts/", include("django.contrib.auth.urls")),
    path(
        "entity/<int:pk>/",
        GetEntityGeneric.as_view(),
        name="GetEntityGeneric",
    ),
    path("api/dumpdata", Dumpdata.as_view()),
]

if "apis_fulltext_download" in settings.INSTALLED_APPS:
    urlpatterns.append(
        path(
            "fulltext_download/",
            include("apis_fulltext_download.urls", namespace="apis_fulltext_download"),
        )
    )

if settings.DEBUG:
    if "debug_toolbar" in settings.INSTALLED_APPS:
        import debug_toolbar

        urlpatterns = [
            re_path(r"^__debug__/", include(debug_toolbar.urls))
        ] + urlpatterns
