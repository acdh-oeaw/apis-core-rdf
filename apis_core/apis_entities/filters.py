import logging

from collections import OrderedDict

import django_filters
from django.conf import settings
from django.db.models import JSONField

from apis_core.utils import caching
from apis_core.utils.settings import get_entity_settings_by_modelname
from apis_core.utils.filtermethods import (
    related_entity_name,
    related_property_name,
)

# The following classes define the filter sets respective to their models.
# Also by what was enabled in the global settings file (or disabled by not explicitley enabling it).
# Hence by default all filters of all model's fields (automatically generated) and all filters manually defined below
# are at first created and then deleted by what was enabled in the settings file
#
# There is a few overrides happening here, which are in order:
# 1.) The filters defined in GenericListFilter
# 2.) The filters automatically defined in model specific ListFilters (by stating exclude = [] in the Meta class)
# 3.) The filters manually defined in model specific ListFilters (by manual field definitions in the Filter class itself)
# If anything is redefined in a step further it overrides the field from the step before
#
# Additionally, in the global settings file:
# The filters defined there can provide a dictionary which can have a "method" or "label" key-value pair
# where then such a key-value from the settings is overriding the respective key-value of a filter defined in this module
# (e.g. using a different method)
fields_to_exclude = getattr(settings, "APIS_RELATIONS_FILTER_EXCLUDE", [])


class GenericEntityListFilter(django_filters.FilterSet):
    """
    Entity fields by which a given entity's list view can be
    filtered on the frontend.

    Combines config options in an app's settings file with entity-specific
    settings defined in models.
    """

    fields_to_exclude = getattr(settings, "APIS_RELATIONS_FILTER_EXCLUDE", [])

    related_entity_name = django_filters.CharFilter(
        method=related_entity_name, label="Related entity"
    )
    related_property_name = django_filters.CharFilter(
        method=related_property_name, label="Related property"
    )

    # TODO: look into how the date values can be intercepted so that they can be parsed with the same logic as in edit forms
    start_date = django_filters.DateFromToRangeFilter()
    end_date = django_filters.DateFromToRangeFilter()

    class Meta:
        # exclude all hardcoded fields or nothing, however this exclude is only defined here as a temporary measure in
        # order to load all filters of all model fields by default so that they are available in the first place.
        # Later those which are not referenced in the settings file will be removed again
        exclude = fields_to_exclude
        filter_overrides = {
            JSONField: {
                "filter_class": django_filters.CharFilter,
                "extra": lambda f: {
                    "lookup_expr": "icontains",
                },
            }
        }

    def __init__(self, *args, **kwargs):
        # call super init foremost to create dictionary of filters which will be processed further below
        super().__init__(*args, **kwargs)
        self.entity_class = self.Meta.model
        self.filters = self.set_and_sort_filters(self.filters)

    def set_and_sort_filters(self, filters):
        """
        Check for existence of "list_filters" setting for an entity
        and return an ordered dictionary containing filters for
        applicable fields plus pre-set filters defined for all entities
        (in GenericEntityListFilter's Meta class).

        :param default_filters: dictionary of filters created
                                on filter class instantiation;
                                includes: GenericListFilter, specific
                                model ListFilter and their defaults

        :return: ordered dictionary with tuples of field names
                 and filters defined for them
        """
        sorted_filters = OrderedDict()

        # fields by which entity lists should not be filterable
        list_filters_exclude = [
            "self_contenttype",
            "review",
            "start_date",
            "start_start_date",
            "start_end_date",
            "end_date",
            "end_start_date",
            "end_end_date",
            "notes",
            "text",
            "published",
            "status",
            "references",
        ]
        entity_settings = get_entity_settings_by_modelname(self.entity_class.__name__)
        list_filters = entity_settings.get("list_filters", {})
        list_filters_exclude.extend(entity_settings.get("list_filters_exclude", []))

        # The `list_filters` setting of an entity defines both the order of filters and it allows to define additional filters
        # A filter is defined by a name and a dict describing its attributes
        # If the name refers to an existing filter, the attributes are used to update that filter
        # If the name does *not* refer to an existing field, then a new filter is created based on the `filter` key
        # The attributes and filters are the ones listed in https://django-filter.readthedocs.io/en/stable/ref/filters.html
        for filter_name in list_filters:
            filter_definition = list_filters[filter_name]
            if filter_name in filters:
                sorted_filters[filter_name] = filters.pop(filter_name)
                if isinstance(filter_definition, dict):
                    for key, value in filter_definition.items():
                        setattr(sorted_filters[filter_name], key, value)
            elif (
                isinstance(filter_definition, dict)
                and "filter" in filter_definition.keys()
            ):
                attrs = {
                    x: filter_definition[x] for x in filter_definition if x != "filter"
                }
                f = getattr(django_filters, filter_definition["filter"])(**attrs)
                sorted_filters[filter_name] = f

        unused_filters = set(list_filters.keys()) ^ set(sorted_filters.keys())
        for unused_filter in unused_filters:
            logging.error(
                "Unusable filter in setting for %s.%s: %s",
                self.entity_class.__module__,
                self.entity_class.__name__,
                unused_filter,
            )

        if "__defaults__" not in list_filters_exclude:
            for f_name, f_filter in filters.items():
                if f_name not in list_filters_exclude:
                    sorted_filters[f_name] = f_filter

        return sorted_filters


def get_list_filter_of_entity(entity):
    """
    Main method to be called somewhere else in the codebase in order to get the FilterClass respective to the entity string input

    :param entity: str: type of entity
    :return: Entity specific FilterClass
    """

    entity_class = caching.get_entity_class_of_name(entity)
    entity_list_filter_class = entity_class.get_entity_list_filter()
    if entity_list_filter_class is None:

        class AdHocEntityListFilter(GenericEntityListFilter):
            class Meta(GenericEntityListFilter.Meta):
                model = entity_class

        entity_list_filter_class = AdHocEntityListFilter

    return entity_list_filter_class
