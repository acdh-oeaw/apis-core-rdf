from django.urls import path, re_path

from . import rel_views
from . import views
from apis_core.apis_entities.autocomplete3 import PropertyAutocomplete

app_name = "apis_relations"

urlpatterns = [
    path(
        "ajax/get/", views.get_form_ajax, name="get_form_ajax"
    ),  # rel_form_logic_breadcrumb (for refinding the implicit connections)
    re_path(
        r"^ajax/save/(?P<entity_type>\w+)/(?P<kind_form>\w+)/(?P<SiteID>[0-9]+)(?:/(?P<ObjectID>[0-9]*))?/$",
        # r'^ajax/save/(?P<entity_type>\w+)/(?P<kind_form>\w+)/(?P<SiteID>[0-9]+)/$', # working without ObjectID
        # r'^ajax/save/(?P<entity_type>\w+)/(?P<kind_form>\w+)/(?P<SiteID>[0-9]+)/(?P<abcde>[0])/$',
        # r'^ajax/save/(?P<entity_type>\w+)/$',
        # r'^ajax/save/(?P<entity_type>\w+)/$',
        views.save_ajax_form,
        name="save_ajax_form",  # rel_form_logic_breadcrumb (for refinding the implicit connections)
    ),
    re_path(
        r"^(?P<entity>[a-z0-9_]+)/list/$",
        rel_views.GenericRelationView.as_view(),
        name="generic_relations_list",
    ),
    re_path(
        r"^(?P<entity>[a-z0-9_]+)/(?P<pk>[0-9]+)/detail$",
        rel_views.GenericRelationDetailView.as_view(),
        name="generic_relations_detail_view",
    ),
    re_path(
        r"^autocomplete/(?P<entity_self>[a-zA-Z0-9-_]+)/(?P<entity_other>[a-zA-Z0-9-_]+)/$",
        PropertyAutocomplete.as_view(),
        name="generic_property_autocomplete",
    ),
    path("<int:instanceid>", views.TripleFromInstance.as_view()),
    path(
        "<int:instanceid>/<int:entity_contenttypeid>",
        views.TripleFromInstanceToEntity.as_view(),
        name="triplefrominstancetoentity",
    ),
    path(
        "<int:instanceid>/<int:entity_contenttypeid>/partial",
        views.TripleFromInstanceToEntityPartial.as_view(),
        name="triplefrominstancetoentitypartial",
    ),
    path("<int:pk>/delete", views.TripleDelete.as_view(), name="tripledelete"),
]
