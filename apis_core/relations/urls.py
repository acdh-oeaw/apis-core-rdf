from django.urls import include, path
from . import views

# app_name = "apis_relations2"

urlpatterns = [
    path("relations/all", views.RelationView.as_view(), name="relation"),
    path(
        "relations/<int:contenttype>/",
        include(
            [
                path("", views.RelationView.as_view(), name="relation"),
                path(
                    "<int:fromcontenttype>/<int:fromoid>",
                    views.RelationView.as_view(),
                    name="relation",
                ),
                path(
                    "<int:fromcontenttype>/<int:fromoid>/<int:tocontenttype>",
                    views.RelationView.as_view(),
                    name="relation",
                ),
                path(
                    "<int:fromcontenttype>/<int:fromoid>/<int:tocontenttype>/inverted",
                    views.RelationView.as_view(inverted=True),
                    name="relationinverted",
                ),
            ]
        ),
    ),
    path(
        "relation/<int:pk>/update",
        views.RelationUpdate.as_view(),
        name="relationupdate",
    ),
    path(
        "relation/<int:pk>/delete",
        views.RelationDelete.as_view(),
        name="relationdelete",
    ),
]
