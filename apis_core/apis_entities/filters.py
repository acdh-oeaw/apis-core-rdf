from functools import reduce
import importlib

import django_filters
from django.conf import settings
from django.db.models import Q

from apis_core.apis_metainfo.models import Collection
from apis_core.apis_entities.models import AbstractEntity, TempEntityClass

from collections import OrderedDict

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

# TODO __sresch__ : Turn the logic of returing a filter object into a singleton pattern to avoid redundant instantiations
# TODO __sresch__ : use the order of list of filter fields in settings


#######################################################################
#
#   Generic super class for sharing filters accross all entities
#
#######################################################################

# TODO __sresch__ : Do this better
fields_to_exclude = getattr(settings, "APIS_RELATIONS_FILTER_EXCLUDE", [])


class GenericEntityListFilter(django_filters.FilterSet):
    """
    Entity fields by which a given entity's list view can be
    filtered on the frontend.

    Combines config options in an app's settings file with entity-specific
    settings defined in models.
    """
    fields_to_exclude = getattr(settings, "APIS_RELATIONS_FILTER_EXCLUDE", [])

    # add default labels to form fields on frontend
    name = django_filters.CharFilter(method="name_label_filter", label="Name or label")
    related_entity_name = django_filters.CharFilter(method="related_entity_name_method", label="Related entity")
    related_property_name = django_filters.CharFilter(method="related_property_name_method", label="Related property")

    collection = django_filters.ModelMultipleChoiceFilter(queryset=Collection.objects.all())

    # TODO __sresch__ : look into how the date values can be intercepted so that they can be parsed with the same logic as in edit forms
    start_date = django_filters.DateFromToRangeFilter()
    end_date = django_filters.DateFromToRangeFilter()

    class Meta:
        model = TempEntityClass
        # exclude all hardcoded fields or nothing, however this exclude is only defined here as a temporary measure in
        # order to load all filters of all model fields by default so that they are available in the first place.
        # Later those which are not referenced in the settings file will be removed again
        exclude = fields_to_exclude

    def __init__(self, *args, **kwargs):
        # call super init foremost to create dictionary of filters which will be processed further below
        super().__init__(*args, **kwargs)
        self.entity_class = self.Meta.model
        self.filters = self.set_sort_filters(self.filters)

    def set_sort_filters(self, default_filters):
        """
        Check for existence of "list_filters" setting for an entity class
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
        field_filters = OrderedDict()

        try:
            fields = self.entity_class.entity_settings['list_filters']
            if fields == ['name', 'related_entity_name', 'related_property_name']:
                # for AbstractEntity, certain fields are defined to be filterable by default;
                # ignore these for the purpose of sorting field names for filtering
                fields = []
        except KeyError as e:
            fields = []
        except Exception as e:
            raise e

        # fields by which entity lists should not be filterable
        ignore_fields = [
            "self_content_type",
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

        for f in fields:
            if type(f) == str and f in default_filters:
                field_filters[f] = default_filters[f]
            elif type(f) == dict:
                field_name = list(f)[0]

                if field_name in default_filters:
                    filter_settings = f[field_name]

                    if "method" in filter_settings:
                        default_filters[field_name].method = filter_settings["method"]

                    if "label" in filter_settings:
                        default_filters[field_name].label = filter_settings["label"]

                    field_filters[field_name] = default_filters[field_name]

            else:
                raise ValueError(
                    f"Filters for individual entities need to be of type "
                    f"string or dictionary.\n"
                    f"Got instead: {type(f)}"
                 )

        for f_name, f_filter in default_filters.items():
            if f_name not in ignore_fields and f_name not in field_filters:
                field_filters[f_name] = f_filter

        return field_filters

        # __before_rdf_refactoring__
        # temporary hack replacement old
        #
        # enabled_filters = settings.APIS_ENTITIES[self.Meta.model.__name__]["list_filters"]
        #
        # filter_dict_tmp = {}
        #
        # for enabled_filter in enabled_filters:
        #
        #     if type(enabled_filter) == str and enabled_filter in default_filter_dict:
        #         # If string then just use it, if a filter with such a name is already defined
        #
        #         filter_dict_tmp[enabled_filter] = default_filter_dict[enabled_filter]
        #
        #
        #     elif type(enabled_filter) == dict:
        #         # if a dictionary, then look further into if there is a method or label which overrides the defaults
        #
        #         enabled_filter_key = list(enabled_filter.keys())[0]
        #
        #         if enabled_filter_key in default_filter_dict:
        #
        #             # get the dictionary which contains potential method or label overrides
        #             enabled_filter_settings_dict = enabled_filter[enabled_filter_key]
        #
        #             if "method" in enabled_filter_settings_dict:
        #                 default_filter_dict[enabled_filter_key].method = enabled_filter_settings_dict["method"]
        #
        #             if "label" in enabled_filter_settings_dict:
        #                 default_filter_dict[enabled_filter_key].label = enabled_filter_settings_dict["label"]
        #
        #             filter_dict_tmp[enabled_filter_key] = default_filter_dict[enabled_filter_key]
        #
        #     else:
        #         raise ValueError(
        #             "Expected either str or dict as type for an individual filter in the settings file."
        #             f"\nGot instead: {type(enabled_filter)}"
        #          )
        #
        # return filter_dict_tmp

        # temporary hack replacement end


    def construct_lookup(self, value):
        """
        Parses user input for wildcards and returns a tuple containing the interpreted django lookup string and the trimmed value
        E.g.
            'example' -> ('__icontains', 'example')
            '*example' -> ('__iendswith', 'example')
            'example*' -> ('__istartswith', 'example')
            '"example"' -> ('__iexact', 'example')

        :param value : str : text to be parsed for *
        :return: (lookup : str, value : str)
        """

        if value.startswith("*") and not value.endswith("*"):
            value = value[1:]
            return "__iendswith", value

        elif not value.startswith("*") and value.endswith("*"):
            value = value[:-1]
            return "__istartswith", value

        elif value.startswith('"') and value.endswith('"'):
            value = value[1:-1]
            return "__iexact", value

        else:
            if value.startswith("*") and value.endswith("*"):
                value = value[1:-1]
            return "__icontains", value

    def name_label_filter(self, queryset, name, value):
        # TODO __sresch__ : include alternative names queries
        lookup, value = self.construct_lookup(value)

        queryset_related_label = queryset.filter(**{"label__label"+lookup : value})
        queryset_self_name = queryset.filter(**{name+lookup : value})

        return (queryset_related_label|queryset_self_name).distinct().all()

    def related_entity_name_method(self, queryset, name, value):
        # __before_rdf_refactoring__
        #
        # """
        # Searches through the all name fields of all related entities of a given queryset
        #
        # For performance reasons it was not sensible to use django's usual lookup foreign key fields
        # (e.g. Person.objects.filter(personwork__related_work__name__icontains=value))
        # Because such naive (but convenient) django ORM approach starts from a given model, goes to the related relation,
        # goes to the related entity and searches therein. But such lookups create a lot of joins in the underlying sql,
        # which get expensive very fast.
        #
        # So the following algorithms reverses this order and always selects primary keys which are then used further to look
        # for related models.
        # Basically what the following does is:
        # step 1: looks up the search value in tempentity class (since all entities inherit from there) and selects their primary keys
        # step 2: uses the keys from step 1 to filter for related relations and selects their primary keys
        # step 3: uses the keys from step 2 to filter for related entities
        # step 4: merge the results from step 3 into one queryset and returns this.
        #
        # :param queryset: the queryset currently to be filtered on
        # :param name: Here not used, because this method filters on names of related entities
        # :param value: The value to be filtered for, input by the user or a programmatic call
        # :return: filtered queryset
        # """
        #
        # # step 1
        # # first find all tempentities where the lookup and value applies, select only their primary keys.
        # lookup, value = self.construct_lookup(value)
        # tempentity_hit = TempEntityClass.objects.filter(**{"name" + lookup: value}).values_list("pk", flat=True)
        #
        # # list for querysets where relations will be saved which are related to the primary keys of the tempentity list above
        # related_relations_to_hit_list = []
        #
        # # step 2
        # # iterate over every relation related to the current queryset model (e.g for Person: PersonWork, PersonPerson, etc)
        # for relation_class in queryset.model.get_related_relation_classes():
        #
        #     # get the related classes and lookup names of the current relation
        #     # (e.g. for PersonWork: class Person, class Work, "related_person", "related_work")
        #     related_entity_classA = relation_class.get_related_entity_classA()
        #     related_entity_classB = relation_class.get_related_entity_classB()
        #     related_entity_field_nameA = relation_class.get_related_entity_field_nameA()
        #     related_entity_field_nameB = relation_class.get_related_entity_field_nameB()
        #
        #     # Within a relation class, there is two fields which relate to entities, check now which of the two
        #     # is the same as the current one.
        #     if queryset.model == related_entity_classA:
        #
        #         # append filtered relation queryset to list for use later
        #         related_relations_to_hit_list.append(
        #             # filter the current relation for if the other related entity's pk is in the hit list of tempentity class
        #             # from before (e.g. if a tempentity's name contains "seu", then its primary key will be used here, to check
        #             # if there is a related entity which has the same primary key.
        #             relation_class.objects.filter(
        #                 **{related_entity_field_nameB + "_id__in": tempentity_hit}
        #             ).values_list(related_entity_field_nameA + "_id", flat=True)
        #         )
        #
        #     # also check the related entity field B (because it can be that both A and B are of the same entity class, e.g. PersonPerson,
        #     # or that only A is the other one, e.g. when filtering for Work within PersonWork, then the other related class is Person)
        #     if queryset.model == related_entity_classB:
        #
        #         # same procedure as above, just with related class and related name being reversed.
        #         related_relations_to_hit_list.append(
        #             relation_class.objects.filter(
        #                 **{related_entity_field_nameA + "_id__in": tempentity_hit}
        #             ).values_list(related_entity_field_nameB + "_id", flat=True)
        #         )
        #
        #     # A safety check which should never arise. But if it does, we know there is something wrong with the automated wiring of
        #     # entities and their respective relation classes (e.g. for Person, there should never be EventWork arising here)
        #     if queryset.model != related_entity_classA and queryset.model != related_entity_classB:
        #
        #         raise ValueError("queryset model class has a wrong relation class associated!")
        #
        # # step 3
        # # Filter the entity queryset for each of the resulting relation querysets produced in the loop before
        # queryset_filtered_list = [ queryset.filter(pk__in=related_relation) for related_relation in related_relations_to_hit_list ]
        #
        # # step 4
        # # merge them all
        # result = reduce( lambda a,b : a | b, queryset_filtered_list).distinct()
        #
        # return result
        #
        # __after_rdf_refactoring__
        lookup, value = self.construct_lookup(value)

        queryset = queryset.filter(
            Q(**{f"triple_set_from_obj__subj__name{lookup}": value})
            | Q(**{f"triple_set_from_subj__obj__name{lookup}": value})
        ).distinct()

        return queryset

    def related_property_name_method(self, queryset, name, value):
        # __before_rdf_refactoring__
        #
        # """
        # Searches through the all name fields of all related relationtypes of a given queryset
        #
        # The following logic is almost identical to the one in method 'related_entity_name_method', so please look up its
        # comments for documentational purpose therein.
        #
        # Differences are commented however.
        #
        # :param queryset: the queryset currently to be filtered on
        # :param name: Here not used, because this method filters on names of related relationtypes
        # :param value: The value to be filtered for, input by the user or a programmatic call
        # :return: filtered queryset
        # """
        #
        # lookup, value = self.construct_lookup(value)
        #
        # # look up through name and name_reverse of Property
        # property_hit = (
        #     Property.objects.filter(**{"name" + lookup: value}).values_list("pk", flat=True) |
        #     Property.objects.filter(**{"name_reverse" + lookup: value}).values_list("pk", flat=True)
        # ).distinct()
        #
        # related_relations_to_hit_list = []
        #
        # for relation_class in queryset.model.get_related_relation_classes():
        #
        #     related_entity_classA = relation_class.get_related_entity_classA()
        #     related_entity_classB = relation_class.get_related_entity_classB()
        #     related_entity_field_nameA = relation_class.get_related_entity_field_nameA()
        #     related_entity_field_nameB = relation_class.get_related_entity_field_nameB()
        #
        #     if queryset.model == related_entity_classA:
        #
        #         # Only difference to method 'related_entity_name_method' is that the lookup is done on 'relation_type_id'
        #         related_relations_to_hit_list.append(
        #             relation_class.objects.filter(
        #                 **{"relation_type_id__in": property_hit}
        #             ).values_list(related_entity_field_nameA + "_id", flat=True)
        #         )
        #
        #     if queryset.model == related_entity_classB:
        #
        #         # Only difference to method 'related_entity_name_method' is that the lookup is done on 'relation_type_id'
        #         related_relations_to_hit_list.append(
        #             relation_class.objects.filter(
        #                 **{"relation_type_id__in": property_hit}
        #             ).values_list(related_entity_field_nameB + "_id", flat=True)
        #         )
        #
        #     if queryset.model != related_entity_classA and queryset.model != related_entity_classB:
        #
        #         raise ValueError("queryset model class has a wrong relation class associated!")
        #
        # queryset_filtered_list = [ queryset.filter(pk__in=related_relation) for related_relation in related_relations_to_hit_list ]
        #
        # result = reduce( lambda a,b : a | b, queryset_filtered_list).distinct()
        #
        # return result
        #
        # __after_rdf_refactoring__
        lookup, value = self.construct_lookup(value)

        queryset = queryset.filter(
            Q(**{f"triple_set_from_obj__prop__name{lookup}": value})
            | Q(**{f"triple_set_from_obj__prop__name_reverse{lookup}": value})
            | Q(**{f"triple_set_from_subj__prop__name{lookup}": value})
            | Q(**{f"triple_set_from_subj__prop__name_reverse{lookup}": value})
        ).distinct()

        return queryset

    def related_arbitrary_model_name(self, queryset, name, value):
        """
        Searches through an arbitrarily related model on its name field.

        Note that this works only if
            * the related model has a field 'name'
            * the filter using this method has the same name as the field of the model on which the filter is applied.
                (E.g. the field 'profession' on a person relates to another model: the professiontype. Here the filter on a person
                must also be called 'profession' as the field 'profession' exists within the person model and is then used to search in.
                Using this example of professions, such a lookup would be generated: Person.objects.filter(profession__name__... ) )
        """

        lookup, value = self.construct_lookup(value)

        # name variable is the name of the filter and needs the corresponding field within the model
        return queryset.filter( **{ name + "__name" + lookup : value } )



#######################################################################
#
#   Overriding Entity filter classes
#
#######################################################################

# __before_rdf_refactoring__
#
# class PersonListFilter(GenericListFilter):
#
#     gender = django_filters.ChoiceFilter(choices=(('', 'any'), ('male', 'male'), ('female', 'female')))
#     profession = django_filters.CharFilter(method="related_arbitrary_model_name")
#     title = django_filters.CharFilter(method="related_arbitrary_model_name")
#     name = django_filters.CharFilter(method="person_name_filter", label="Name or Label of person")
#
#
#     # TODO __sresch__ : look into how the meta class can be inherited from the superclass so that the Meta class' exclude attribute must not be defined multiple times
#     class Meta:
#         model = Person
#         # exclude all hardcoded fields or nothing, however this exclude is only defined here as a temporary measure in
#         # order to load all filters of all model fields by default so that they are available in the first place.
#         # Later those which are not referenced in the settings file will be removed again
#         exclude = GenericListFilter.fields_to_exclude
#
#
#     def person_name_filter(self, queryset, name, value):
#
#         lookup, value = self.construct_lookup(value)
#
#         queryset_related_label=queryset.filter(**{"label__label"+lookup : value})
#         queryset_self_name=queryset.filter(**{name+lookup : value})
#         queryset_first_name=queryset.filter(**{"first_name"+lookup : value})
#
#         # return QuerySet.union(queryset_related_label, queryset_self_name, queryset_first_name)
#         return (queryset_related_label | queryset_self_name | queryset_first_name).distinct().all()
#
#
#
# class PlaceListFilter(GenericListFilter):
#
#     # TODO __sresch__ : decide on margin tolerance of input, for now the number must be precise
#     lng = django_filters.NumberFilter(label='Longitude')
#     lat = django_filters.NumberFilter(label='Latitude')
#
#     class Meta:
#         model = Place
#         # exclude all hardcoded fields or nothing, however this exclude is only defined here as a temporary measure in
#         # order to load all filters of all model fields by default so that they are available in the first place.
#         # Later those which are not referenced in the settings file will be removed again
#         exclude = GenericListFilter.fields_to_exclude
#
#
#
# class InstitutionListFilter(GenericListFilter):
#
#     class Meta:
#         model = Institution
#         # exclude all hardcoded fields or nothing, however this exclude is only defined here as a temporary measure in
#         # order to load all filters of all model fields by default so that they are available in the first place.
#         # Later those which are not referenced in the settings file will be removed again
#         exclude = GenericListFilter.fields_to_exclude
#
#
#
# class EventListFilter(GenericListFilter):
#
#     class Meta:
#         model = Event
#         # exclude all hardcoded fields or nothing, however this exclude is only defined here as a temporary measure in
#         # order to load all filters of all model fields by default so that they are available in the first place.
#         # Later those which are not referenced in the settings file will be removed again
#         exclude = GenericListFilter.fields_to_exclude
#
#
#
# class WorkListFilter(GenericListFilter):
#
#     kind = django_filters.ModelChoiceFilter(queryset=WorkType.objects.all())
#
#     class Meta:
#         model = Work
#         # exclude all hardcoded fields or nothing, however this exclude is only defined here as a temporary measure in
#         # order to load all filters of all model fields by default so that they are available in the first place.
#         # Later those which are not referenced in the settings file will be removed again
#         exclude = GenericListFilter.fields_to_exclude
#
# __after_rdf_refactoring__
def get_list_filter_of_entity(entity):
    """
    Main method to be called somewhere else in the codebase in order to get the FilterClass respective to the entity string input

    :param entity: str: type of entity
    :return: Entity specific FilterClass
    """

    entity_class = AbstractEntity.get_entity_class_of_name(entity)

    entity_list_filter_class = entity_class.get_entity_list_filter()

    if entity_list_filter_class is None:
        class AdHocEntityListFilter(GenericEntityListFilter):
            class Meta(GenericEntityListFilter.Meta):
                model = entity_class

        entity_list_filter_class = AdHocEntityListFilter

    return entity_list_filter_class
