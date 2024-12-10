from drf_spectacular.utils import extend_schema_field
from rest_framework.serializers import SerializerMethodField

from apis_core.generic.serializers import SimpleObjectSerializer, serializer_factory


class RelationSerializer(SimpleObjectSerializer):
    subj = SerializerMethodField()
    obj = SerializerMethodField()

    class Meta:
        fields = SimpleObjectSerializer.Meta.fields + ["subj", "obj"]

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
