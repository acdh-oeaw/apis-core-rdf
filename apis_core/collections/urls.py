from django.urls import path

from . import views

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
]
