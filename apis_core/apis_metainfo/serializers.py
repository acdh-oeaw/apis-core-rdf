from django.contrib.contenttypes.models import ContentType
from rest_framework import serializers

from .models import Collection, Uri

from apis_core.generic.serializers import GenericHyperlinkedModelSerializer


class CollectionSerializer(serializers.HyperlinkedModelSerializer):
    url = serializers.HyperlinkedIdentityField(
        view_name="apis:apis_api:text-detail", lookup_field="pk"
    )
    collection_type = serializers.HyperlinkedRelatedField(
        view_name="apis:apis_api:collectiontype-detail",
        lookup_field="pk",
        read_only=True,
    )
    parent_class = serializers.HyperlinkedRelatedField(
        view_name="apis:apis_api:collection-detail", lookup_field="pk", read_only=True
    )

    class Meta:
        fields = ["url", "name", "description", "collection_type", "parent_class"]
        model = Collection


class UriSerializer(GenericHyperlinkedModelSerializer):
    url = serializers.HyperlinkedIdentityField(
        view_name="apis:apis_api:uri-detail", lookup_field="pk"
    )

    class Meta:
        fields = "__all__"
        model = Uri


class ContentTypeSerializer(serializers.HyperlinkedModelSerializer):
    url = serializers.HyperlinkedIdentityField(
        view_name="apis:apis_api:contenttype-detail", lookup_field="pk"
    )

    class Meta:
        fields = "__all__"
        model = ContentType
