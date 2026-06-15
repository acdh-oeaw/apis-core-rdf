from django.urls import path

from apis_core.entities.views import CanonicalEntity, E53_PlaceMap

urlpatterns = [
    path("entity/<int:pk>", CanonicalEntity.as_view(), name="canonical-entity"),
    path("<contenttype:contenttype>/map", E53_PlaceMap.as_view(), name="e53_place_map"),
]
