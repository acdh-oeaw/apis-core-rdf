from django.contrib.contenttypes.models import ContentType
from django.shortcuts import get_object_or_404
from rdflib import Graph, Literal, Namespace, URIRef
from rdflib.namespace import GEO, OWL, RDF, RDFS
from rest_framework.reverse import reverse
from rest_framework.serializers import (
    BaseSerializer,
    CharField,
    HyperlinkedModelSerializer,
    HyperlinkedRelatedField,
    IntegerField,
    Serializer,
    SerializerMethodField,
)

from apis_core.utils.settings import apis_base_uri, rdf_namespace_prefix


class GenericHyperlinkedRelatedField(HyperlinkedRelatedField):
    def get_url(self, obj, view_name, request, format):
        contenttype = ContentType.objects.get_for_model(obj, for_concrete_model=True)
        url_kwargs = {"contenttype": contenttype, "pk": obj.pk}
        return reverse(
            "apis_core:generic:genericmodelapi-detail",
            kwargs=url_kwargs,
            request=request,
            format=format,
        )

    def use_pk_only_optimization(self):
        # We have the complete object instance already. We don't need
        # to run the 'only get the pk for this relationship' code.
        return False


class GenericHyperlinkedIdentityField(GenericHyperlinkedRelatedField):
    def __init__(self, view_name=None, **kwargs):
        assert view_name is not None, "The `view_name` argument is required."
        kwargs["read_only"] = True
        kwargs["source"] = "*"
        super().__init__(view_name, **kwargs)


class GenericHyperlinkedModelSerializer(HyperlinkedModelSerializer):
    serializer_related_field = GenericHyperlinkedRelatedField
    serializer_url_field = GenericHyperlinkedIdentityField


def serializer_factory(
    model, serializer=GenericHyperlinkedModelSerializer, fields="__all__", **kwargs
):
    defaultmeta = type(str("Meta"), (object,), {"fields": fields})
    meta = getattr(serializer, "Meta", defaultmeta)
    meta.model = model
    serializer = type(
        str("%sModelSerializer" % model._meta.object_name),
        (serializer,),
        {"Meta": meta},
    )
    return serializer


class ContentTypeInstanceSerializer(Serializer):
    id = IntegerField(required=True)
    content_type = CharField(required=True)

    def to_internal_value(self, data):
        data = super().to_internal_value(data)
        app_label, model = data.get("content_type").split(".")
        content_type = get_object_or_404(ContentType, app_label=app_label, model=model)
        return get_object_or_404(content_type.model_class(), pk=data.get("id"))


class SimpleObjectSerializer(Serializer):
    url = GenericHyperlinkedIdentityField(
        view_name="apis_core:generic:genericmodelapi-detail"
    )
    label = SerializerMethodField()
    content_type_key = SerializerMethodField()
    content_type_name = SerializerMethodField()

    class Meta:
        fields = ["url", "label", "content_type_key", "content_type_name"]

    def get_label(self, obj) -> str:
        return str(obj)

    def get_content_type_key(self, obj) -> str:
        content_type = ContentType.objects.get_for_model(obj)
        return f"{content_type.app_label}.{content_type.model}"

    def get_content_type_name(self, obj) -> str:
        content_type = ContentType.objects.get_for_model(obj)
        return content_type.name


class GenericModelCidocSerializer(BaseSerializer):
    def __init__(self, *args, **kwargs):
        self.base_uri = f"{apis_base_uri()}"
        self.rdf_nsp_base = rdf_namespace_prefix()
        self.appellation_nsp_prefix = f"{self.rdf_nsp_base}-appellation"
        self.attr_nsp_prefix = f"{self.rdf_nsp_base}-attr"
        super().__init__(*args, **kwargs)

    def to_representation(self, instance):
        g = Graph()
        content_type = ContentType.objects.get_for_model(instance)

        crm_namespace = Namespace("http://www.cidoc-crm.org/cidoc-crm/")
        g.namespace_manager.bind("crm", crm_namespace, replace=True)
        g.namespace_manager.bind("owl", OWL, replace=True)
        g.namespace_manager.bind("geo", GEO, replace=True)

        appellation_namespace = Namespace(f"{self.base_uri}/appellation/")
        g.namespace_manager.bind(
            self.appellation_nsp_prefix, appellation_namespace, replace=True
        )
        attributes_namespace = Namespace(f"{self.base_uri}/attributes/")
        g.namespace_manager.bind(
            self.attr_nsp_prefix, attributes_namespace, replace=True
        )

        self.instance_nsp_prefix = f"{self.rdf_nsp_base}-{content_type.name.lower()}"
        instance_namespace = Namespace(self.base_uri + instance.get_listview_url())
        g.namespace_manager.bind(self.instance_nsp_prefix, instance_namespace)

        self.instance_uri = URIRef(instance_namespace[str(instance.id)])

        # Add sameAs links
        for uri in instance.uri_set.all():
            uri_ref = URIRef(uri.uri)
            g.add((self.instance_uri, OWL.sameAs, uri_ref))

        # Add properties
        self.appellation_uri = URIRef(appellation_namespace[str(instance.id)])
        g.add(
            (
                self.appellation_uri,
                RDF.type,
                crm_namespace.E33_E41_Linguistic_Appellation,
            )
        )
        g.add(
            (
                self.instance_uri,
                crm_namespace.P1_is_identified_by,
                self.appellation_uri,
            )
        )
        g.add((self.appellation_uri, RDFS.label, Literal(str(instance))))

        return g
