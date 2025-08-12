from django.contrib.contenttypes.models import ContentType
from django.db.models import Q
from django_filters import CharFilter, MultipleChoiceFilter

from apis_core.apis_metainfo.models import RootObject
from apis_core.generic.filtersets import GenericFilterSet
from apis_core.generic.helpers import generate_search_filter
from apis_core.relations.forms import RelationFilterSetForm
from apis_core.relations.models import Relation
from apis_core.relations.utils import get_all_relation_subj_and_obj


class EntityFilter(CharFilter):
    """
    Custom CharFilter that uses the generate_search_filter helper
    to search in all instances inheriting from RootObject and then
    uses those results to only list relations that point to one of
    the results.
    """

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.extra["help_text"] = "Searches in subclasses of RootObject"

    def _search_all_entities(self, value) -> list[str]:
        q = Q()
        for content_type in get_all_relation_subj_and_obj():
            name = content_type.model
            q |= Q(**{f"{name}__isnull": False}) & generate_search_filter(
                content_type.model_class(), value, prefix=f"{name}__"
            )
        return RootObject.objects_inheritance.filter(q).values_list("pk", flat=True)

    def filter(self, qs, value):
        if value:
            all_entities = self._search_all_entities(value)
            return qs.filter(**{f"{self.field_name}_object_id__in": all_entities})
        return qs


class SubjObjClassFilter(MultipleChoiceFilter):
    """
    Custom MultipleChoiceFilter
    * it lists model classes as choices, that are in some way
      connected to a relation, either as subj or as obj
    * it filters relations by the content types of the connected
      subjects and objects
    """

    def __init__(self, models, *args, **kwargs):
        super().__init__(*args, **kwargs)
        content_types = [ContentType.objects.get_for_model(model) for model in models]
        self.extra["choices"] = [(item.id, item.name) for item in content_types]

    def filter(self, qs, value: list[str] | None):
        # value is the list of contenttypes ids
        if value:
            return qs.filter(Q(**{f"{self.field_name}_content_type__in": value}))
        return qs


class RelationFilterSet(GenericFilterSet):
    """
    Override the GenericFilterSet that is created for the Relation model.
    It does not really make sense to filter for content type id and object id,
    so we exclude those.
    Instead, we add a multiple choice filter for object and subject class, that
    only lists those choices that actually exists (meaning the classes that are
    actually set as subj or obj in some relation).
    Additionaly, we add a search filter, that searches in instances connected
    to relations (this does only work for instances inheriting from RootObject).
    """

    subj_search = EntityFilter(
        field_name="subj",
        label="Subject search",
    )
    obj_search = EntityFilter(
        field_name="obj",
        label="Object search",
    )

    class Meta:
        exclude = [
            "subj_object_id",
            "subj_content_type",
            "obj_object_id",
            "obj_content_type",
        ]
        form = RelationFilterSetForm

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if model := getattr(self.Meta, "model", False):
            if model is Relation and "collections" in self.filters:
                del self.filters["collections"]
            all_models = [ct.model_class() for ct in get_all_relation_subj_and_obj()]
            subj_models = getattr(model, "subj_model", all_models)
            obj_models = getattr(model, "obj_model", all_models)
            if isinstance(subj_models, list):
                self.filters["subj_class"] = SubjObjClassFilter(
                    field_name="subj", label="Subject class", models=subj_models
                )
            if isinstance(obj_models, list):
                self.filters["obj_class"] = SubjObjClassFilter(
                    field_name="obj", label="Object Class", models=obj_models
                )
