import django_filters
from django.contrib.contenttypes.models import ContentType
from django.db.models import Case, Q, Value, When
from django.db.models.functions import Concat

from apis_core.apis_entities.utils import get_entity_classes
from apis_core.apis_metainfo.models import RootObject
from apis_core.generic.helpers import generate_search_filter


def related_entity(queryset, name, value):
    from apis_core.apis_relations.models import Triple

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
        from apis_core.apis_relations.models import Property

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
        from apis_core.apis_relations.models import Property

        if value:
            p = Property.objects.get(name_forward=value)
            queryset = queryset.filter(triple_set_from_subj__prop=p).distinct()
        return queryset
