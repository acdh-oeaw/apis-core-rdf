from django.urls import include, path
from . import views

urlpatterns = [
    path(
        "<contenttype:contenttype>/",
        include(
            [
                path(
                    "create/<contenttype:fromcontenttype>/<int:frompk>/<contenttype:tocontenttype>",
                    views.RelationForm.as_view(),
                    name="relationform",
                ),
            ]
        ),
    ),
    path("list/<contenttype:fromcontenttype>/<int:frompk>/<contenttype:tocontenttype>",
         views.RelationList.as_view(),
         name="relations_list",
    ),
]
