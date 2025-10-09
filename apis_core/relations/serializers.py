from drf_spectacular.utils import extend_schema_field
from rest_framework.serializers import SerializerMethodField

from apis_core.generic.serializers import (
    GenericHyperlinkedModelSerializer,
    SimpleObjectSerializer,
    serializer_factory,
)


class RelationSerializer(GenericHyperlinkedModelSerializer):
    subj = SerializerMethodField()
    obj = SerializerMethodField()

    class Meta:
        exclude = (
            "subj_content_type",
            "subj_object_id",
            "obj_content_type",
            "obj_object_id",
        )

    @extend_schema_field(SimpleObjectSerializer())
    def get_subj(self, obj):
        if obj.subj:
            serializer = serializer_factory(type(obj.subj), SimpleObjectSerializer)
            return serializer(
                obj.subj, context={"request": self.context["request"]}
            ).data

    @extend_schema_field(SimpleObjectSerializer())
    def get_obj(self, obj):
        if obj.obj:
            serializer = serializer_factory(type(obj.obj), SimpleObjectSerializer)
            return serializer(
                obj.obj, context={"request": self.context["request"]}
            ).data
