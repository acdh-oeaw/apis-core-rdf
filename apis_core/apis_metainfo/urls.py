from django.urls import path

from . import views

app_name = "apis_metainfo"

urlpatterns = [
    path("uri/getorcreate/", views.UriGetOrCreate.as_view(), name="uri_get_or_create"),
]
