from django.conf import settings
from django.urls import path

from . import api_views

app_name = "apis_entities"

urlpatterns = [
    path("savenetworkfiles/", api_views.SaveNetworkFiles.as_view()),
    path(
        "getorcreateentity/",
        api_views.GetOrCreateEntity.as_view(),
        name="GetOrCreateEntity",
    ),
    path(
        "entity/<int:pk>/",
        api_views.GetEntityGeneric.as_view(),
        name="GetEntityGeneric",
    ),
    # path(r'getrelatedplaces/', api_views.GetRelatedPlaces.as_view(), name="GetRelatedPlaces"),
    # path(r'lifepath/<int:pk>/', api_views.LifePathViewset.as_view(), name="Lifepathviewset")
]
