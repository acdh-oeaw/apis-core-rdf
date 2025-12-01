from django.urls import path

from apis_core.entities.views import CanonicalEntity

urlpatterns = [
    path("entity/<int:pk>", CanonicalEntity.as_view(), name="canonical-entity")
]
