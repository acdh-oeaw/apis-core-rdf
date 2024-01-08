import os
import pickle
from datetime import date

from django.conf import settings
from rdflib import XSD, Graph, Literal, Namespace, URIRef, ConjunctiveGraph, OWL
from rdflib.namespace import DCTERMS, VOID
from rdflib import plugin
from rdflib.void import generateVoID
from rest_framework import renderers

from apis_core.utils.renderers.tei import TeiRenderer
from .api_mappings.cidoc_mapping import m_person, m_place, m_work, m_institution

PROJECT_METADATA = getattr(settings, "PROJECT_DEFAULT_MD", {})


base_uri = getattr(settings, "APIS_BASE_URI", "http://apis.info")
if base_uri.endswith("/"):
    base_uri = base_uri[:-1]
lang = getattr(settings, "LANGUAGE_CODE", "de")


class EntityToTEI(TeiRenderer):
    def render(self, data, media_type=None, renderer_context=None):
        self.template_name = f"apis_entities/tei/{data['entity_type']}.xml"
        return super().render(data, media_type, renderer_context)


class EntityToCIDOC(renderers.BaseRenderer):

    media_type = "text/rdf"

    ent_func = {
        "Person": m_person,
        "Place": m_place,
        "Work": m_work,
        "Institution": m_institution,
    }

    def render(
        self,
        data1,
        media_type=None,
        renderer_context=None,
        format_1=None,
        binary=False,
        store=False,
        named_graph=None,
        provenance=False,
    ):
        if isinstance(data1, dict):
            data1 = [data1]
        if format_1 is not None:
            self.format = format_1
        cidoc = Namespace("http://www.cidoc-crm.org/cidoc-crm/")
        geo = Namespace("http://www.opengis.net/ont/geosparql#")
        frbroo = Namespace("http://iflastandards.info/ns/fr/frbr/frbroo#")
        if not store:
            store = plugin.get("Memory", Store)()
        if named_graph:
            uri_entities = URIRef(named_graph)
        else:
            uri_entities = URIRef(f"{base_uri}/entities#")
        g = Graph(store, identifier=uri_entities)
        g.bind("cidoc", cidoc, override=False)
        g.bind("geo", geo, override=False)
        g.bind("owl", OWL, override=False)
        g.bind("frbroo", frbroo, override=False)
        ns = {"cidoc": cidoc, "geo": geo, "frbroo": frbroo}
        if type(data1) == list:
            for data in data1:
                g, ent = self.ent_func[data["entity_type"]](
                    g, ns, data, drill_down=True
                )
        elif type(data1) == str:
            directory = os.fsencode(data1)
            for fn in os.listdir(directory):
                with open(os.path.join(directory, fn), "rb") as inf:
                    data2 = pickle.load(inf)
                    for data in data2:
                        g, ent = self.ent_func[data["entity_type"]](
                            g, ns, data, drill_down=True
                        )
        if provenance:
            g_prov = Graph(
                store, identifier=URIRef("https://omnipot.acdh.oeaw.ac.at/provenance")
            )
            g_prov.bind("dct", DCTERMS, override=False)
            g_prov.bind("void", VOID, override=False)
            g_prov.add(
                (
                    uri_entities,
                    DCTERMS.title,
                    Literal(PROJECT_METADATA["title"], lang=lang),
                )
            )
            g_prov.add(
                (
                    uri_entities,
                    DCTERMS.description,
                    Literal(PROJECT_METADATA["description"], lang=lang),
                )
            )
            g_prov.add(
                (
                    uri_entities,
                    DCTERMS.creator,
                    Literal(PROJECT_METADATA["author"], lang=lang),
                )
            )
            g_prov.add(
                (uri_entities, DCTERMS.publisher, Literal("ACDH-OeAW", lang=lang))
            )
            g_prov.add((uri_entities, DCTERMS.source, URIRef(base_uri)))
            g_prov.add(
                (
                    uri_entities,
                    DCTERMS.created,
                    Literal(str(date.today()), datatype=XSD.date),
                )
            )
            g_prov, g = generateVoID(g, dataset=uri_entities, res=g_prov)
        g_all = ConjunctiveGraph(store=store)
        if binary:
            return g_all, store
        return g_all.serialize(format=self.format.split("+")[-1])


class EntityToCIDOCXML(EntityToCIDOC):

    format = "rdf+xml"


class EntityToCIDOCN3(EntityToCIDOC):

    format = "rdf+n3"


class EntityToCIDOCNQUADS(EntityToCIDOC):

    format = "rdf+nquads"


class EntityToCIDOCTURTLE(EntityToCIDOC):

    format = "rdf+turtle"
