from django.urls import path, re_path

from apis_core.apis_entities.autocomplete3 import PropertyAutocomplete

from . import views

app_name = "apis_relations"

urlpatterns = [
    path("ajax/get/", views.get_form_ajax, name="get_form_ajax"),
    re_path(
        r"^ajax/save/(?P<entity_type>\w+)/(?P<kind_form>\w+)/(?P<SiteID>[0-9]+)(?:/(?P<ObjectID>[0-9]*))?/$",
        views.save_ajax_form,
        name="save_ajax_form",
    ),
    re_path(
        r"^(?P<entity>[a-z0-9_]+)/list/$",
        views.GenericRelationView.as_view(),
        name="generic_relations_list",
    ),
    re_path(
        r"^autocomplete/(?P<entity_self>[a-zA-Z0-9-_]+)/(?P<entity_other>[a-zA-Z0-9-_]+)/$",
        PropertyAutocomplete.as_view(),
        name="generic_property_autocomplete",
    ),
]
