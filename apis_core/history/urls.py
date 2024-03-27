from apis_core.history import views
from apis_core.history.api_views import (
    EntityHistoryLogs,
    GenericHistoryLog,
    TempTripleHistoryLogs,
)
from django.urls import path

app_name = "history"


urlpatterns = [
    path(
        "change_history/<contenttype:contenttype>/<int:pk>/",
        views.ChangeHistoryView.as_view(),
        name="change_history",
    ),
    path(
        "add_new_version/<contenttype:contenttype>/<int:pk>/",
        views.create_new_version,
        name="add_new_history_version",
    ),
    path(
        "api/version_log/<contenttype:contenttype>/<int:pk>/",
        EntityHistoryLogs.as_view(),
        name="entityhistorylog",
    ),
    path(
        "api/version_log/temp_triple/<int:pk>/",
        TempTripleHistoryLogs.as_view(),
        name="temptriplehistorylog",
    ),
    path(
        "api/entity_combined/<contenttype:contenttype>/<int:pk>/",
        GenericHistoryLog.as_view(),
        name="generichistorylog",
    ),
]
