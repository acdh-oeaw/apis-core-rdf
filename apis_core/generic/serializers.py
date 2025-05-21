import re

from AcdhArcheAssets.uri_norm_rules import get_rules
from django.contrib.contenttypes.models import ContentType
from django.shortcuts import get_object_or_404
from rdflib import Graph, Literal, Namespace, URIRef
from rdflib.namespace import OWL, RDF, RDFS
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

from apis_core.generic.utils.rdf_namespace import APPELLATION, ATTRIBUTES, CRM
from apis_core.utils.settings import rdf_namespace_prefix


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
    model,
    serializer=GenericHyperlinkedModelSerializer,
    action="detail",
    fields="__all__",
    **kwargs,
):
    defaultmeta = type(str("Meta"), (object,), {"fields": fields})
    meta = getattr(serializer, "Meta", defaultmeta)
    meta.model = model
    serializer = type(
        str("%s%sModelSerializer" % (model._meta.object_name, action)),
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
        self.rdf_nsp_base = rdf_namespace_prefix()
        self.appellation_nsp_prefix = f"{self.rdf_nsp_base}-appellation"
        self.attr_nsp_prefix = f"{self.rdf_nsp_base}-attr"
        super().__init__(*args, **kwargs)

    def create_sameas(self, g, instance):
        # add the ID as APIS Identifier
        apis_id = URIRef(ATTRIBUTES[f"apis-identifier_{instance.pk}"])
        g.add((apis_id, RDF.type, CRM.E42_Identifier))
        g.add((apis_id, RDFS.label, Literal(instance.pk)))

        # APIS internal identifier type
        apis_id_type = URIRef(ATTRIBUTES["apis-identifier_type"])
        g.add((apis_id, CRM.P2_has_type, apis_id_type))
        g.add((apis_id_type, RDF.type, CRM.E55_Type))
        g.add((apis_id_type, RDFS.label, Literal("APIS internal identifier")))
        g.add((self.instance_uri, CRM.P1_is_identified_by, apis_id))

        for uri in instance.uri_set():
            g.add((self.instance_uri, OWL.sameAs, URIRef(uri.uri)))

            for x in get_rules():
                if m := re.match(x["match"], uri.uri):
                    id_type = URIRef(ATTRIBUTES[x["name"] + "-identifier_type"])
                    g.add((id_type, RDF.type, CRM.E55_Type))
                    g.add((id_type, RDFS.label, Literal(x["name"] + " ID")))
                    id_uri = URIRef(
                        ATTRIBUTES[x["name"] + f"-identifier_{instance.pk}"]
                    )
                    g.add((id_uri, RDF.type, CRM.E42_Identifier))
                    g.add((id_uri, CRM.P2_has_type, id_type))
                    g.add(
                        (
                            self.instance_uri,
                            CRM.P1_is_identified_by,
                            id_uri,
                        )
                    )
                    g.add((id_uri, RDFS.label, Literal(m[1])))

        return g

    def to_representation(self, instance):
        g = Graph()

        g.namespace_manager.bind("crm", CRM, replace=True)
        g.namespace_manager.bind("owl", OWL, replace=True)

        g.namespace_manager.bind(self.appellation_nsp_prefix, APPELLATION, replace=True)
        g.namespace_manager.bind(self.attr_nsp_prefix, ATTRIBUTES, replace=True)

        self.instance_namespace = Namespace(instance.get_namespace_uri())
        g.namespace_manager.bind(
            instance.get_namespace_prefix(), self.instance_namespace
        )

        self.instance_uri = URIRef(self.instance_namespace[str(instance.id)])

        # Add properties
        self.appellation_uri = URIRef(APPELLATION[str(instance.id)])
        g.add(
            (
                self.appellation_uri,
                RDF.type,
                CRM.E33_E41_Linguistic_Appellation,
            )
        )
        g.add(
            (
                self.instance_uri,
                CRM.P1_is_identified_by,
                self.appellation_uri,
            )
        )
        g.add((self.appellation_uri, RDFS.label, Literal(str(instance))))
        g.add((self.instance_uri, RDFS.label, Literal(str(instance))))
        # Add RDF types
        for rdf_type in instance.get_rdf_types():
            g.add((self.instance_uri, RDF.type, rdf_type))
        # Add sameAs links
        g = self.create_sameas(g, instance)

        return g
