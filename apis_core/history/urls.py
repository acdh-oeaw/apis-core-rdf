from django.urls import path

from apis_core.history import views

app_name = "history"


urlpatterns = [
    path(
        "<contenttype:contenttype>/<int:pk>/history",
        views.HistoryView.as_view(),
        name="history",
    ),
    path(
        "<contenttype:contenttype>/<int:pk>/reset",
        views.HistoryReset.as_view(),
        name="reset",
    ),
]
