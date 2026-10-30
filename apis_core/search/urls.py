from django.urls import path

from . import views

app_name = "search"

urlpatterns = [
    path("search", views.SearchView.as_view(), name="search"),
    path(
        "autocomplete/suggestions",
        views.AutocompleteSuggestions.as_view(),
        name="autocomplete-suggestions",
    ),
    path(
        "autocomplete/singleselect/<int:pk>",
        views.AutocompleteSingleSelect.as_view(),
        name="autocomplete-singleselect",
    ),
]
