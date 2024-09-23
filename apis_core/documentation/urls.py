from django.urls import path

from . import views

urlpatterns = [
    path("documentation", views.Documentation.as_view(), name="documentation"),
]
