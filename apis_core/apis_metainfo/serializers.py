from rest_framework import serializers

from .models import Uri

from apis_core.generic.serializers import GenericHyperlinkedModelSerializer


class UriSerializer(GenericHyperlinkedModelSerializer):
    url = serializers.HyperlinkedIdentityField(
        view_name="apis_core:apis_api:uri-detail", lookup_field="pk"
    )

    class Meta:
        fields = "__all__"
        model = Uri
