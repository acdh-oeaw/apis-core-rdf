import logging

from rdflib import Graph
from rest_framework import renderers

logger = logging.getLogger(__name__)


class GenericRDFBaseRenderer(renderers.BaseRenderer):
    def render(self, data, accepted_media_type=None, renderer_context=None):
        g = Graph()
        for result in data.get("results", []):
            match result:
                case tuple(_, _, _):
                    g.add(result)
                case other:
                    logger.debug("Could not add %s to RDF graph: not a tuple", other)
        return g.serialize(format=self.media_type)


class GenericRDFXMLRenderer(GenericRDFBaseRenderer):
    media_type = "application/rdf+xml"
    format = "rdf+xml"


class GenericRDFTurtleRenderer(GenericRDFBaseRenderer):
    media_type = "text/turtle"
    format = "rdf+turtle"


class GenericRDFN3Renderer(GenericRDFBaseRenderer):
    media_type = "text/n3"
    format = "rdf+n3"
