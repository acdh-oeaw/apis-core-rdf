from django.urls import path

from apis_core.apis_entities.api_views import GetEntityGeneric, ListEntityGeneric

# from .views import ReversionCompareView TODO: add again when import is fixed
from apis_core.apis_entities.views import E53_PlaceMap, EntitiesAutocomplete

api_routes = [
    path("entities/", ListEntityGeneric.as_view()),
    path(
        "entity/<int:pk>/",
        GetEntityGeneric.as_view(),
        name="GetEntityGeneric",
    ),
]


app_name = "apis_entities"

urlpatterns = [
    path("autocomplete/", EntitiesAutocomplete.as_view(), name="autocomplete"),
    path("<contenttype:contenttype>/map", E53_PlaceMap.as_view(), name="e53_place_map"),
]
