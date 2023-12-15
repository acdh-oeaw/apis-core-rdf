from django.urls import include, path

from . import views, edit_generic, detail_generic, merge_views
from .autocomplete3 import (
    GenericEntitiesAutocomplete,
    GenericNetworkEntitiesAutocomplete,
)

# from .views import ReversionCompareView TODO: add again when import is fixed
from .edit_generic import GenericEntitiesCreateStanbolView
from .api_views import GetOrCreateEntity

app_name = "apis_entities"

entity_patterns = [
    path(
        "list/",
        views.GenericListViewNew.as_view(),
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
        "entity/<slug:entity>/",
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
