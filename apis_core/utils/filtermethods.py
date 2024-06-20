"""
This module contains filter functions that can be used by django-filter filters
See https://django-filter.readthedocs.io/en/main/ref/filters.html#method
"""

from django.db.models import Q


# should return tuple[str, str] once we are >=3.9
def construct_lookup(value: str) -> tuple:
    """
    Helper method to parse input values and construct field lookups
    (https://docs.djangoproject.com/en/4.2/ref/models/querysets/#field-lookups)
    Parses user input for wildcards and returns a tuple containing the
    interpreted django lookup string and the trimmed value
    E.g.

    - ``example`` -> ``('__icontains', 'example')``
    - ``*example*`` -> ``('__icontains', 'example')``
    - ``*example`` -> ``('__iendswith', 'example')``
    - ``example*``-> ``('__istartswith', 'example')``
    - ``"example"`` -> ``('__iexact', 'example')``

    :param str value: text to be parsed for ``*``
    :return: a tuple containing the lookup type and the value without modifiers
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


def flexible_string(queryset, name, value):
    """
    filter method for filtering arbitrary fields using :func:`construct_lookup`
    """
    lookup, value = construct_lookup(value)
    return queryset.filter(**{name + lookup: value})


# filtermethods for specific usecases:


# TODO RDF: Check if this should be removed or adapted
def related_entity_name(queryset, name, value):
    """
    filter on the name of a related entity using :func:`construct_lookup`
    """
    lookup, value = construct_lookup(value)

    queryset = queryset.filter(
        Q(**{f"triple_set_from_obj__subj__name{lookup}": value})
        | Q(**{f"triple_set_from_subj__obj__name{lookup}": value})
    ).distinct()

    return queryset


def related_property_name(queryset, name, value):
    """
    filter on the name of a related property using :func:`construct_lookup`
    """
    lookup, value = construct_lookup(value)

    queryset = queryset.filter(
        Q(**{f"triple_set_from_obj__prop__name_forward{lookup}": value})
        | Q(**{f"triple_set_from_obj__prop__name_reverse{lookup}": value})
        | Q(**{f"triple_set_from_subj__prop__name_forward{lookup}": value})
        | Q(**{f"triple_set_from_subj__prop__name_reverse{lookup}": value})
    ).distinct()

    return queryset


def related_arbitrary_model_name(queryset, name, value):
    """
    Searches through an arbitrarily related model on its name field using :func:`construct_lookup`.
    Note that this works only if

    - the related model has a field 'name'
    - the filter using this method has the same name as the field of the model on which the filter is applied.

    (E.g. the field ``profession`` on a person relates to another model: the professiontype. Here the filter on a person
    must also be called ``profession`` as the field ``profession`` exists within the person model and is then used to search in.
    Using this example of professions, such a lookup would be generated: ``Person.objects.filter(profession__name__... )`` )
    """

    lookup, value = construct_lookup(value)

    # name variable is the name of the filter and needs the corresponding field within the model
    return queryset.filter(**{name + "__name" + lookup: value})


def name_label_filter(queryset, name, value):
    lookup, value = construct_lookup(value)

    queryset_related_label = queryset.filter(**{"label__label" + lookup: value})
    queryset_self_name = queryset.filter(**{name + lookup: value})

    return (queryset_related_label | queryset_self_name).distinct().all()
