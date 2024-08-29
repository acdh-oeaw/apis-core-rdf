from django.urls import path

from . import views

app_name = "collections"

urlpatterns = [
    path(
        "collectionobjecttoggle/<int:content_type_id>/<int:object_id>/<int:collection>",
        views.CollectionToggle.as_view(),
        name="collectiontoggle",
    ),
    path(
        "collectionobjectparent/<int:content_type_id>/<int:object_id>/<int:collectionobject>",
        views.CollectionObjectParent.as_view(),
        name="collectionobjectparent",
    ),
    path(
        "collectionsessiontoggle/<int:skoscollection>",
        views.CollectionSessionToggle.as_view(),
        name="collectionsessiontoggle",
    ),
]
