from django.contrib.contenttypes.models import ContentType
from django.shortcuts import get_object_or_404
from django.urls import include, path, register_converter
from rest_framework import routers

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
        return get_object_or_404(ContentType, app_label=app_label, model=model)

    def to_url(self, value):
        return f"{value.app_label}.{value.model}"


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
            ]
        ),
    ),
    path("api/<contenttype:contenttype>/", include(router.urls)),
]
