from django.contrib.contenttypes.models import ContentType
from django.shortcuts import get_object_or_404
from django.urls import include, path, register_converter
from django.http import Http404
from rest_framework import routers
from .abc import GenericModel

from apis_core.generic import views, api_views

app_name = "generic"


class ContenttypeConverter:
    """
    A converter that converts from a string representation of a
    model (`app_label.model`) to the actual Django model class.
    """

    regex = r"\w+\.\w+"

    def to_python(self, value):
        app_label, model = value.split(".")
        contenttype = get_object_or_404(ContentType, app_label=app_label, model=model)
        if issubclass(contenttype.model_class(), GenericModel):
            return contenttype
        raise Http404

    def to_url(self, value):
        if isinstance(value, ContentType):
            return f"{value.app_label}.{value.model}"
        if isinstance(value, str):
            return value


register_converter(ContenttypeConverter, "contenttype")

router = routers.DefaultRouter()
router.register(r"", api_views.ModelViewSet, basename="genericmodelapi")

urlpatterns = [
    path("overview/", views.Overview.as_view(), name="overview"),
    path(
        "<contenttype:contenttype>/",
        include(
            [
                path("", views.List.as_view(), name="list"),
                path("<int:pk>", views.Detail.as_view(), name="detail"),
                path("create", views.Create.as_view(), name="create"),
                path("delete/<int:pk>", views.Delete.as_view(), name="delete"),
                path("update/<int:pk>", views.Update.as_view(), name="update"),
                path("autocomplete", views.Autocomplete.as_view(), name="autocomplete"),
                path("import", views.Import.as_view(), name="import"),
                path(
                    "autocomplete/externalonly",
                    views.Autocomplete.as_view(),
                    {"external_only": True},
                    name="autocompleteexternalonly",
                ),
            ]
        ),
    ),
    path("api/<contenttype:contenttype>/", include(router.urls)),
]
