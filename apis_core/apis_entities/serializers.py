from rdflib import Literal, Namespace, URIRef
from rdflib.namespace import GEO, RDF, RDFS
from rest_framework import serializers

from apis_core.generic.serializers import (
    GenericHyperlinkedIdentityField,
    GenericModelCidocSerializer,
)


class MinimalEntitySerializer(serializers.Serializer):
    uri = GenericHyperlinkedIdentityField(
        view_name="apis_core:generic:genericmodelapi-detail"
    )
    name = serializers.SerializerMethodField(method_name="get_name")

    def get_name(self, object) -> str:
        return str(object)


class E53_PlaceCidocSerializer(GenericModelCidocSerializer):
    def to_representation(self, instance):
        g = super().to_representation(instance)

        crm_namespace = Namespace("http://www.cidoc-crm.org/cidoc-crm/")
        attributes_namespace = Namespace(f"{self.base_uri}/attributes/")
        g.add((self.instance_uri, RDF.type, crm_namespace.E53_Place))
        if instance.latitude is not None and instance.longitude is not None:
            node_spaceprimitive = attributes_namespace[f"spaceprimitive.{instance.id}"]
            g.add(
                (
                    self.instance_uri,
                    crm_namespace.P168_place_is_defined_by,
                    node_spaceprimitive,
                )
            )
            g.add(
                (
                    node_spaceprimitive,
                    RDF.type,
                    crm_namespace.E94_Space_Primitive,
                )
            )
            g.add(
                (
                    node_spaceprimitive,
                    crm_namespace.P168_place_is_defined_by,
                    Literal(
                        (
                            f"Point ( {'+' if instance.longitude > 0 else ''}{instance.longitude} {'+' if instance.latitude > 0 else ''}{instance.latitude} )"
                        ),
                        datatype=GEO.wktLiteral,
                    ),
                )
            )
        return g


class E21_PersonCidocSerializer(GenericModelCidocSerializer):
    def to_representation(self, instance):
        g = super().to_representation(instance)

        crm_namespace = Namespace("http://www.cidoc-crm.org/cidoc-crm/")
        g.add((self.instance_uri, RDF.type, crm_namespace.E21_Person))
        g.add(
            (
                self.instance_uri,
                RDFS.label,
                Literal(f"{instance.forename} {instance.surname}"),
            )
        )

        if hasattr(instance, "forename"):
            forename_uri = URIRef(self.appellation_namespace[f"forename_{instance.id}"])
            g.add(
                (
                    forename_uri,
                    RDF.type,
                    crm_namespace.E33_E41_Linguistic_Appellation,
                )
            )
            g.add(
                (
                    self.appellation_uri,
                    crm_namespace.P106_is_composed_of,
                    forename_uri,
                )
            )
            g.add((forename_uri, RDFS.label, Literal(instance.forename)))

        if hasattr(instance, "surname"):
            surname_uri = URIRef(self.appellation_namespace[f"surname_{instance.id}"])
            g.add(
                (
                    surname_uri,
                    RDF.type,
                    crm_namespace.E33_E41_Linguistic_Appellation,
                )
            )
            g.add(
                (
                    self.appellation_uri,
                    crm_namespace.P106_is_composed_of,
                    surname_uri,
                )
            )
            g.add((surname_uri, RDFS.label, Literal(instance.surname)))

        return g
