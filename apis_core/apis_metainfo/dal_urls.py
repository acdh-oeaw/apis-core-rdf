from django.urls import path

from . import dal_views

app_name = "apis_metainfo"

urlpatterns = [
    path(
        "tempentity-autocomplete/",
        dal_views.TempEntityClassAC.as_view(),
        name="apis_tempentity-autocomplete",
    )
]
