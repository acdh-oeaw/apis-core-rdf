from django.urls import path, re_path

from . import views

app_name = "apis_metainfo"

urlpatterns = [
    path("apis/metainfo/uri/", views.UriListView.as_view(), name="uri_browse"),
    path("uri/detail/<int:pk>", views.UriDetailView.as_view(), name="uri_detail"),
    path("uri/create/", views.UriCreate.as_view(), name="uri_create"),
    path("uri/edit/<int:pk>", views.UriUpdate.as_view(), name="uri_edit"),
    path("uri/delete/<int:pk>", views.UriDelete.as_view(), name="uri_delete"),
    path("uri/getorcreate/", views.UriGetOrCreate.as_view(), name="uri_get_or_create"),
]
