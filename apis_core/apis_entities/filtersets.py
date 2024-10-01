import django_filters
from django.conf import settings
from django.contrib.contenttypes.models import ContentType
from django.db import models
from django.db.models import Case, Q, Value, When
from django.db.models.functions import Concat
from django.forms import DateInput
from django.utils.encoding import force_str
from simple_history.utils import get_history_manager_for_model

from apis_core.apis_entities.utils import get_entity_classes
from apis_core.apis_metainfo.models import RootObject
from apis_core.apis_relations.models import Property, Triple
from apis_core.generic.filtersets import GenericFilterSet, GenericFilterSetForm
from apis_core.generic.helpers import default_search_fields, generate_search_filter

ABSTRACT_ENTITY_COLUMNS_EXCLUDE = [
    "rootobject_ptr",
    "self_contenttype",
    "triple_set_from_subj",
    "triple_set_from_obj",
    "uri",
]

ABSTRACT_ENTITY_FILTERS_EXCLUDE = ABSTRACT_ENTITY_COLUMNS_EXCLUDE + [
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


class PropertyChoiceField(django_filters.fields.ModelChoiceField):
    def label_from_instance(self, obj):
        if obj.forward:
            targets = [ct.name for ct in obj.obj_class.all()]
        else:
            targets = [ct.name for ct in obj.subj_class.all()]
        return obj.name + " | " + ", ".join(targets)


class PropertyFilter(django_filters.ModelChoiceFilter):
    """
    A child of ModelChoiceFilter that only works with
    Properties, but in return it filters those so that
    only the Properties are listed that can be connected
    to the `model` given as argument.
    """

    field_class = PropertyChoiceField

    def __init__(self, *args, **kwargs):
        model = kwargs.pop("model", None)
        super().__init__(*args, **kwargs)

        if model is not None:
            ct = ContentType.objects.get_for_model(model)
            self.queryset = (
                Property.objects.all()
                .filter(Q(subj_class=ct) | Q(obj_class=ct))
                .annotate(
                    name=Case(
                        When(
                            obj_class=ct,
                            subj_class=ct,
                            then=Concat("name_forward", Value(" / "), "name_reverse"),
                        ),
                        When(obj_class=ct, then="name_reverse"),
                        When(subj_class=ct, then="name_forward"),
                    ),
                    forward=Case(
                        When(obj_class=ct, then=Value(False)),
                        When(subj_class=ct, then=Value(True)),
                    ),
                )
                .order_by("name")
                .distinct()
            )

    def filter(self, queryset, value):
        if value:
            p = Property.objects.get(name_forward=value)
            queryset = queryset.filter(triple_set_from_subj__prop=p).distinct()
        return queryset


class ModelSearchFilter(django_filters.CharFilter):
    """
    This filter is a customized CharFilter that
    uses the `generate_search_filter` method to
    adapt the search filter to the model that is
    searched.
    It also extracts sets the help text based on
    the fields searched.
    """

    def __init__(self, *args, **kwargs):
        model = kwargs.pop("model", None)
        super().__init__(*args, **kwargs)

        if model is not None and "help_text" not in self.extra:
            field_names = [field.verbose_name for field in default_search_fields(model)]
            # use force_str on the fields verbose names to convert
            # lazy instances to string and join the results
            fields = ", ".join(map(force_str, field_names))
            self.extra["help_text"] = f"Search in fields: {fields}"

    def filter(self, qs, value):
        return qs.filter(generate_search_filter(qs.model, value))


def related_entity(queryset, name, value):
    entities = get_entity_classes()
    q = Q()
    for entity in entities:
        name = entity._meta.model_name
        q |= Q(**{f"{name}__isnull": False}) & generate_search_filter(
            entity, value, prefix=f"{name}__"
        )
    all_entities = RootObject.objects_inheritance.filter(q).values_list("pk", flat=True)
    t = (
        Triple.objects.filter(Q(subj__in=all_entities) | Q(obj__in=all_entities))
        .annotate(
            related=Case(
                When(subj__in=all_entities, then="obj"),
                When(obj__in=all_entities, then="subj"),
            )
        )
        .values_list("related", flat=True)
    )
    return queryset.filter(pk__in=t)


def changed_since(queryset, name, value):
    history = get_history_manager_for_model(queryset.model)
    ids = history.filter(history_date__gt=value).values_list("id", flat=True)
    return queryset.filter(pk__in=ids)


class AbstractEntityFilterSetForm(GenericFilterSetForm):
    columns_exclude = ABSTRACT_ENTITY_COLUMNS_EXCLUDE


class AbstractEntityFilterSet(GenericFilterSet):
    related_entity = django_filters.CharFilter(
        method=related_entity, label="Related entity contains"
    )

    class Meta(GenericFilterSet.Meta):
        form = AbstractEntityFilterSetForm
        exclude = ABSTRACT_ENTITY_FILTERS_EXCLUDE
        filter_overrides = {
            models.CharField: {
                "filter_class": django_filters.CharFilter,
                "extra": lambda f: {
                    "lookup_expr": "icontains",
                },
            },
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.filters["related_property"] = PropertyFilter(
            label="Related Property", model=getattr(self.Meta, "model", None)
        )

        if model := getattr(self.Meta, "model", False):
            self.filters["search"] = ModelSearchFilter(model=model)
            self.filters.move_to_end("search", False)

        if "apis_core.history" in settings.INSTALLED_APPS:
            self.filters["changed_since"] = django_filters.DateFilter(
                label="Changed since",
                widget=DateInput(attrs={"type": "date"}),
                method=changed_since,
            )
