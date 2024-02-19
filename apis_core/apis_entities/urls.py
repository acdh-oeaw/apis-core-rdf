from django.contrib.contenttypes.models import ContentType
from django.http import Http404
from django.urls import include, path, register_converter
from django.shortcuts import get_list_or_404

from .autocomplete3 import (
    GenericNetworkEntitiesAutocomplete,
)

# from .views import ReversionCompareView TODO: add again when import is fixed
from .api_views import GetOrCreateEntity
from apis_core.apis_entities.models import AbstractEntity
from apis_core.generic.views import List, Create, Delete, Detail
from apis_core.apis_entities.views import (
    EntitiesDuplicate,
    EntitiesUpdate,
    EntitiesMerge,
)


class EntityToContenttypeConverter:
    """
    A converter that converts from a the name of an entity class
    (i.e. `person`) to the actual Django model class.
    """

    regex = r"\w+"

    def to_python(self, value):
        candiates = get_list_or_404(ContentType, model=value)
        candiates = list(
            filter(lambda ct: issubclass(ct.model_class(), AbstractEntity), candiates)
        )
        if len(candiates) > 1:
            raise Http404("Multiple entities match the <%s> identifier" % value)
        return candiates[0]

    def to_url(self, value):
        return value


register_converter(EntityToContenttypeConverter, "entitytocontenttype")

app_name = "apis_entities"

entity_patterns = [
    path(
        "list/",
        List.as_view(),
        name="generic_entities_list",
    ),
    path(
        "create/",
        Create.as_view(),
        name="generic_entities_create_view",
    ),
    path(
        "<int:pk>/detail/",
        Detail.as_view(),
        name="generic_entities_detail_view",
    ),
    path(
        "<int:pk>/edit/",
        EntitiesUpdate.as_view(),
        name="generic_entities_edit_view",
    ),
    path(
        "<int:pk>/delete/",
        Delete.as_view(),
        name="generic_entities_delete_view",
    ),
    path(
        "<int:pk>/duplicate/",
        EntitiesDuplicate.as_view(),
        name="generic_entities_duplicate_view",
    ),
    path(
        "<int:pk>/merge/",
        EntitiesMerge.as_view(),
        name="generic_entities_merge_view",
    ),
]

urlpatterns = [
    path(
        "entity/<entitytocontenttype:contenttype>/",
        include(entity_patterns),
    ),
    path(
        "autocomplete-network/<slug:entity>/",
        GenericNetworkEntitiesAutocomplete.as_view(),
        name="generic_network_entities_autocomplete",
    ),
    path(
        "getorcreateentity/",
        GetOrCreateEntity.as_view(),
        name="GetOrCreateEntity",
    ),
]
