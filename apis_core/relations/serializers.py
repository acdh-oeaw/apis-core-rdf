from rest_framework import serializers
from apis_core.generic.serializers import GenericHyperlinkedModelSerializer


class RelationSerializer(GenericHyperlinkedModelSerializer):
    subj = serializers.SerializerMethodField()
    obj = serializers.SerializerMethodField()

    class Meta:
        fields = ["obj", "subj"]

    def get_subj(self, obj):
        return obj.subj.get_api_detail_endpoint()

    def get_obj(self, obj):
        return obj.obj.get_api_detail_endpoint()
