from rest_framework import serializers

from apis_core.generic.serializers import GenericHyperlinkedIdentityField


class MinimalEntitySerializer(serializers.Serializer):
    uri = GenericHyperlinkedIdentityField(
        view_name="apis_core:generic:genericmodelapi-detail"
    )
    name = serializers.SerializerMethodField(method_name="get_name")

    def get_name(self, object) -> str:
        return str(object)
