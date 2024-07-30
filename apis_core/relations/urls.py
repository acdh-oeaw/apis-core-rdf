from django.urls import path

from apis_core.relations.views import CreateRelation, CreateRelationForm, ListRelations

app_name = "relations"

urlpatterns = [
    path(
        "<contenttype:contenttype>/create",
        CreateRelation.as_view(),
        name="create_relation",
    ),
    path(
        "<contenttype:contenttype>/form",
        CreateRelationForm.as_view(),
        name="create_relation_form",
    ),
    path(
        "<contenttype:target_contenttype>/list/<contenttype:object_contenttype>/<int:object_id>",
        ListRelations.as_view(),
        name="list_relations",
    ),
]
