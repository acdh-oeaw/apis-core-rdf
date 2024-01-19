from django.contrib.contenttypes.models import ContentType
from django.http import Http404
from django.urls import include, path, register_converter
from django.shortcuts import get_list_or_404

from . import views, edit_generic, detail_generic, merge_views
from .autocomplete3 import (
    GenericEntitiesAutocomplete,
    GenericNetworkEntitiesAutocomplete,
)

# from .views import ReversionCompareView TODO: add again when import is fixed
from .edit_generic import GenericEntitiesCreateStanbolView
from .api_views import GetOrCreateEntity
from apis_core.generic.views import List
from .models import AbstractEntity


class EntityToContenttypeConverter:
    """
    A converter that converts from a the name of an entity class
    (i.e. `person`) to the actual Django model class.
    """

    regex = r"\w+"

    def to_python(self, value):
        candiates = get_list_or_404(ContentType, model=value)
        candiates = list(
            filter(lambda ct: issubclass(ct.model_class(), AbstractEntity), candiates)
        )
        if len(candiates) > 1:
            raise Http404("Multiple entities match the <%s> identifier" % value)
        return candiates[0]

    def to_url(self, value):
        return value


register_converter(EntityToContenttypeConverter, "entitytocontenttype")


app_name = "apis_entities"

entity_patterns = [
    path(
        "list/",
        List.as_view(),
        name="generic_entities_list",
    ),
    path(
        "create/",
        edit_generic.GenericEntitiesCreateView.as_view(),
        name="generic_entities_create_view",
    ),
    path(
        "<int:pk>/detail/",
        detail_generic.GenericEntitiesDetailView.as_view(),
        name="generic_entities_detail_view",
    ),
    path(
        "<int:pk>/edit/",
        edit_generic.GenericEntitiesEditView.as_view(),
        name="generic_entities_edit_view",
    ),
    path(
        "<int:pk>/delete/",
        edit_generic.GenericEntitiesDeleteView.as_view(),
        name="generic_entities_delete_view",
    ),
    path(
        "<int:pk>/duplicate/",
        edit_generic.GenericEntitiesDuplicateView.as_view(),
        name="generic_entities_duplicate_view",
    ),
]

autocomplete_patterns = [
    path(
        "createstanbol/<slug:entity>/<int:ent_merge_pk>/",
        GenericEntitiesCreateStanbolView.as_view(),
        name="generic_entities_stanbol_create",
    ),
    path(
        "createstanbol/<slug:entity>/",
        GenericEntitiesCreateStanbolView.as_view(),
        name="generic_entities_stanbol_create",
    ),
    path(
        "<slug:entity>/<int:ent_merge_pk>/",
        GenericEntitiesAutocomplete.as_view(),
        name="generic_entities_autocomplete",
    ),
    path(
        "<slug:entity>/<str:db_include>/",
        GenericEntitiesAutocomplete.as_view(),
        name="generic_entities_autocomplete",
    ),
    path(
        "<slug:entity>/",
        GenericEntitiesAutocomplete.as_view(),
        name="generic_entities_autocomplete",
    ),
]

urlpatterns = [
    path(
        "entity/<entitytocontenttype:contenttype>/",
        include(entity_patterns),
    ),
    path(
        "autocomplete/",
        include(autocomplete_patterns),
    ),
    path(
        "autocomplete-network/<slug:entity>/",
        GenericNetworkEntitiesAutocomplete.as_view(),
        name="generic_network_entities_autocomplete",
    ),
    path("place/geojson/", views.getGeoJson, name="getGeoJson"),
    path("merge-objects/", merge_views.merge_objects, name="merge_objects"),
    path(
        "getorcreateentity/",
        GetOrCreateEntity.as_view(),
        name="GetOrCreateEntity",
    ),
]
