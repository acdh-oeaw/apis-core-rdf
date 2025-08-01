from django.urls import path

from . import views

app_name = "collections"

urlpatterns = [
    path(
        "<contenttype:contenttype>/<int:pk>/collections",
        views.CollectionObjectFormView.as_view(),
        name="collectionobjectformview",
    ),
    path(
        "collectionobjecttoggle/<int:content_type_id>/<int:object_id>/<int:collection>",
        views.CollectionToggle.as_view(),
        name="collectiontoggle",
    ),
    path(
        "collectionobjectcollection/<int:content_type_id>/<int:object_id>/<int:collectionobject>",
        views.CollectionObjectCollection.as_view(),
        name="collectionobjectparent",
    ),
    path(
        "collectionsessiontoggle/<int:skoscollection>",
        views.CollectionSessionToggle.as_view(),
        name="collectionsessiontoggle",
    ),
]
