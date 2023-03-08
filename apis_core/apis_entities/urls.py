from django.urls import include, path
from . import views, views2, detail_views, merge_views
from .autocomplete3 import GenericEntitiesAutocomplete, GenericNetworkEntitiesAutocomplete
# from .views import ReversionCompareView TODO: add again when import is fixed
from .views2 import GenericEntitiesCreateStanbolView


app_name = "apis_entities"

entity_patterns = [
    path('list/', views.GenericListViewNew.as_view(),
         name='generic_entities_list',
         ),
    path('create/', views2.GenericEntitiesCreateView.as_view(),
         name='generic_entities_create_view',
         ),
    path('<int:pk>/detail/', detail_views.GenericEntitiesDetailView.as_view(),
         name='generic_entities_detail_view',
         ),
    path('<int:pk>/edit/', views2.GenericEntitiesEditView.as_view(),
         name='generic_entities_edit_view',
         ),
    path('<int:pk>/delete/', views2.GenericEntitiesDeleteView.as_view(),
         name='generic_entities_delete_view',
         ),
]

autocomplete_patterns = [
    path('createstanbol/<slug:entity>/<int:ent_merge_pk>/',
         GenericEntitiesCreateStanbolView.as_view(),
         name='generic_entities_stanbol_create',
         ),
    path('createstanbol/<slug:entity>/',
         GenericEntitiesCreateStanbolView.as_view(),
         name='generic_entities_stanbol_create',
         ),
    path('<slug:entity>/<int:ent_merge_pk>/',
         GenericEntitiesAutocomplete.as_view(),
         name='generic_entities_autocomplete',
         ),
    path('<slug:entity>/<str:db_include>/',
         GenericEntitiesAutocomplete.as_view(),
         name='generic_entities_autocomplete',
         ),
    path('<slug:entity>/',
         GenericEntitiesAutocomplete.as_view(),
         name='generic_entities_autocomplete',
         ),
]

urlpatterns = [
    path('entity/<slug:entity>/', include(entity_patterns), ),
    path('autocomplete/', include(autocomplete_patterns), ),
    path('autocomplete-network/<slug:entity>/',
         GenericNetworkEntitiesAutocomplete.as_view(),
         name='generic_network_entities_autocomplete',
         ),

    # TODO __sresch__ : This seems unused. Remove it once sure
    # url(r"^detail/work/(?P<pk>[0-9]+)$",
    #     detail_generic.WorkDetailView.as_view(), name="work_detail"),

    path('place/geojson/', views.getGeoJson, name='getGeoJson'),
    # __before_rdf_refactoring__
    # url(r"^place/geojson/list/$", views.getGeoJsonList, name="getGeoJsonList"),
    # url(r"^place/network/list/$", views.getNetJsonList, name="getNetJsonList"),
    # url(
    #     r"^resolve/place/(?P<pk>[0-9]+)/(?P<uri>.+)$",
    #     views.resolve_ambigue_place,
    #     name="resolve_ambigue_place",
    # ),

    path('maps/birthdeath/', views.birth_death_map, name='birth_death_map'),
    path('networks/relation_place/', views.pers_place_netw, name='pers_place_netw'),
    path('networks/relation_institution/', views.pers_inst_netw, name='pers_inst_netw'),
    path('networks/generic/', views.generic_network_viz, name='generic_network_viz'),
    #    url(
    #        r'^compare/(?P<app>[a-z_]+)/(?P<kind>[a-z]+)/(?P<pk>\d+)$', ReversionCompareView.as_view()
    #    ),
    path('merge-objects/', merge_views.merge_objects, name='merge_objects'),
]
