from django.contrib.contenttypes.models import ContentType
from django.http import Http404
from django.shortcuts import get_list_or_404
from django.urls import include, path, register_converter

from apis_core.apis_entities.api_views import GetEntityGeneric, ListEntityGeneric

# from .views import ReversionCompareView TODO: add again when import is fixed
from apis_core.apis_entities.models import AbstractEntity
from apis_core.apis_entities.views import (
    EntitiesAutocomplete,
    EntitiesDuplicate,
)

api_routes = [
    path("entities/", ListEntityGeneric.as_view()),
    path(
        "entity/<int:pk>/",
        GetEntityGeneric.as_view(),
        name="GetEntityGeneric",
    ),
]


class EntityToContenttypeConverter:
    """
    A converter that converts from a the name of an entity class
    (i.e. `person`) to the actual Django model class.
    """

    regex = r"\w+"

    def to_python(self, value):
        candiates = get_list_or_404(ContentType, model=value)
        candiates = list(
            filter(
                lambda ct: ct.model_class() is not None
                and issubclass(ct.model_class(), AbstractEntity),
                candiates,
            )
        )
        if len(candiates) > 1:
            raise Http404("Multiple entities match the <%s> identifier" % value)
        return candiates[0]

    def to_url(self, value):
        if isinstance(value, ContentType):
            return value.model
        if isinstance(value, str):
            return value


register_converter(EntityToContenttypeConverter, "entitytocontenttype")

app_name = "apis_entities"

entity_patterns = [
    path(
        "<int:pk>/duplicate/",
        EntitiesDuplicate.as_view(),
        name="generic_entities_duplicate_view",
    ),
]

urlpatterns = [
    path(
        "entity/<entitytocontenttype:contenttype>/",
        include(entity_patterns),
    ),
    path("autocomplete/", EntitiesAutocomplete.as_view(), name="autocomplete"),
]
