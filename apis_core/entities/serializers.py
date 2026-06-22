from rdflib import Literal, Namespace, URIRef
from rdflib.namespace import GEO, RDF, RDFS

from apis_core.generic.serializers import GenericModelCidocSerializer
from apis_core.generic.utils.rdf_namespace import APPELLATION, CRM


class E21_PersonCidocSerializer(GenericModelCidocSerializer):
    def to_representation(self, instance):
        g = super().to_representation(instance)

        if hasattr(instance, "forename"):
            forename_uri = URIRef(APPELLATION[f"forename_{instance.id}"])
            g.add(
                (
                    forename_uri,
                    RDF.type,
                    CRM.E33_E41_Linguistic_Appellation,
                )
            )
            g.add(
                (
                    self.appellation_uri,
                    CRM.P106_is_composed_of,
                    forename_uri,
                )
            )
            g.add((forename_uri, RDFS.label, Literal(instance.forename)))

        if hasattr(instance, "surname"):
            surname_uri = URIRef(APPELLATION[f"surname_{instance.id}"])
            g.add(
                (
                    surname_uri,
                    RDF.type,
                    CRM.E33_E41_Linguistic_Appellation,
                )
            )
            g.add(
                (
                    self.appellation_uri,
                    CRM.P106_is_composed_of,
                    surname_uri,
                )
            )
            g.add((surname_uri, RDFS.label, Literal(instance.surname)))

        PFPG = Namespace("https://pfp-schema.acdh.oeaw.ac.at/types/gender/#")
        g.namespace_manager.bind("pfpg", PFPG, replace=True)
        match getattr(instance, "gender", None):
            case "male":
                g.add((self.instance_uri, RDF.type, PFPG.male))
            case "female":
                g.add((self.instance_uri, RDF.type, PFPG.female))
            case "non-binary":
                g.add((self.instance_uri, RDF.type, PFPG["non-binary"]))
            case "unknown":
                g.add((self.instance_uri, RDF.type, PFPG.unknown))
            case "non-applicable":
                g.add((self.instance_uri, RDF.type, PFPG["non-applicable"]))
        return g


class E53_PlaceCidocSerializer(GenericModelCidocSerializer):
    def to_representation(self, instance):
        g = super().to_representation(instance)

        if instance.latitude is not None and instance.longitude is not None:
            literal_text = f"Point ( {instance.longitude:+} {instance.latitude:+} )"
            literal = Literal(literal_text, datatype=GEO.wktLiteral)
            g.add((self.instance_uri, CRM.P168_place_is_defined_by, literal))
        return g
