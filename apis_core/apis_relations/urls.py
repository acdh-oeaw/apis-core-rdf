from django.conf.urls import url

from . import rel_views
from . import views
from apis_core.apis_entities.autocomplete3 import PropertyAutocomplete

app_name = "apis_relations"

urlpatterns = [
    url(
        r"^ajax/get/$", views.get_form_ajax, name="get_form_ajax"
    ),  # rel_form_logic_breadcrumb (for refinding the implicit connections)
    url(
        r"^ajax/save/(?P<entity_type>\w+)/(?P<kind_form>\w+)/(?P<SiteID>[0-9]+)(?:/(?P<ObjectID>[0-9]*))?/$",
        views.save_ajax_form,
        name="save_ajax_form",  # rel_form_logic_breadcrumb (for refinding the implicit connections)
    ),
    url(
        r"^(?P<entity>[a-z0-9_]+)/list/$",
        rel_views.GenericRelationView.as_view(),
        name="generic_relations_list",
    ),
    url(
        r"^(?P<entity>[a-z0-9_]+)/(?P<pk>[0-9]+)/detail$",
        rel_views.GenericRelationDetailView.as_view(),
        name="generic_relations_detail_view",
    ),
    url(
        r"^autocomplete/(?P<entity_self>[a-zA-Z0-9-_]+)/(?P<entity_other>[a-zA-Z0-9-_]+)/$",
        PropertyAutocomplete.as_view(),
        name="generic_property_autocomplete",
    ),
    url(
        r"^ajax_2_post_reification_form/$",
        views.ajax_2_post_reification_form,
        name="ajax_2_post_reification_form",
    ),
    url(
        r"^ajax_2_delete_reification/$",
        views.ajax_2_delete_reification,
        name="ajax_2_delete_reification",
    ),
    url(
        r"^ajax_2_load_reification_form/$",
        views.ajax_2_load_reification_form,
        name="ajax_2_load_reification_form",
    ),
    url(
        r"^ajax_2_load_triple_form/$",
        views.ajax_2_load_triple_form,
        name="ajax_2_load_triple_form",
    ),
    url(
        r"^ajax_2_delete_triple/$",
        views.ajax_2_delete_triple,
        name="ajax_2_delete_triple",
    ),
    url(
        r"^ajax_2_post_triple_form/$",
        views.ajax_2_post_triple_form,
        name="ajax_2_post_triple_form",
    ),
]
