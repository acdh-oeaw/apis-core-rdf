import django_filters
from django.contrib.contenttypes.models import ContentType
from django.db.models import Q

from apis_core.relations.forms.fields import RelationField
from apis_core.relations.models import Relation


class RelationFilter(django_filters.Filter):
    field_class = RelationField

    def filter(self, qs, value):
        if not value:
            return qs
        relationid, entity_ct_id = value
        subj = Q()
        obj = Q()
        if entity_ct_id:
            content_type_id, entity_id = entity_ct_id.split("_")
            entity = (
                ContentType.objects.get(pk=content_type_id)
                .model_class()
                .objects.get(pk=entity_id)
            )
            subj = Q(subj_content_type=content_type_id, subj_object_id=entity.id)
            obj = Q(obj_content_type=content_type_id, obj_object_id=entity.id)
        relation_model = Relation
        if relationid:
            relation_model = ContentType.objects.get(pk=relationid).model_class()
        obj_rels = relation_model.objects.filter(subj).values_list(
            "obj_object_id", flat=True
        )
        subj_rels = relation_model.objects.filter(obj).values_list(
            "subj_object_id", flat=True
        )
        possible_ids = set(list(subj_rels) + list(obj_rels))
        return qs.filter(pk__in=possible_ids)
