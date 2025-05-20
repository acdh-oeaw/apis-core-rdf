from django.urls import path

from apis_core.history import views
from apis_core.history.api_views import (
    EntityHistoryLogs,
    GenericHistoryLog,
)

app_name = "history"


urlpatterns = [
    path(
        "<contenttype:contenttype>/<int:pk>/history",
        views.HistoryView.as_view(),
        name="history",
    ),
    path(
        "api/version_log/<contenttype:contenttype>/<int:pk>/",
        EntityHistoryLogs.as_view(),
        name="entityhistorylog",
    ),
    path(
        "api/entity_combined/<contenttype:contenttype>/<int:pk>/",
        GenericHistoryLog.as_view(),
        name="generichistorylog",
    ),
    path(
        "<contenttype:contenttype>/<int:pk>/reset",
        views.HistoryReset.as_view(),
        name="reset",
    ),
]
