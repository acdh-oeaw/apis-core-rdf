import logging

from rdflib import Graph
from rest_framework import renderers
from rest_framework.exceptions import APIException

logger = logging.getLogger(__name__)


class GenericRDFBaseRenderer(renderers.BaseRenderer):
    """
    Base class to render RDF graphs to various formats.
    This renderer expects the serialized data to either be a rdflib grap **or**
    to contain a list of rdflib graphs. If it works with a list of graphs, those
    are combined to one graph.
    This graph is then serialized and the result is returned. The serialization
    format can be set using the `rdflib_format` attribute. If this is not set, the
    `format` attribute of the renderer is used as serialization format (this is the
    format as it is used by the Django Rest Framework for content negotiation.
    """

    format = "ttl"
    rdflib_format = None

    def render(self, data, accepted_media_type=None, renderer_context=None):
        result = Graph()

        match data:
            case {"results": results, **rest}:  # noqa: F841
                # Handle case where data is a dict with multiple graphs
                for graph in results:
                    if isinstance(graph, Graph):
                        # Merge triples
                        for triple in graph:
                            result.add(triple)
                        # Merge namespace bindings
                        for prefix, namespace in graph.namespaces():
                            result.bind(prefix, namespace, override=False)
            case {"detail": detail}:
                raise APIException(detail)
            case Graph():
                # Handle case where data is a single graph
                result = data
                # Ensure namespaces are properly bound in the single graph case
                for prefix, namespace in data.namespaces():
                    result.bind(prefix, namespace, override=False)
            case _:
                raise ValueError(
                    "Invalid data format. Expected rdflib Graph or dict with 'results' key containing graphs"
                )
        serialization_format = self.rdflib_format or self.format
        return result.serialize(format=serialization_format)


class GenericRDFTurtleRenderer(GenericRDFBaseRenderer):
    format = "ttl"
    media_type = "text/turtle"
    rdflib_format = "turtle"


class GenericRDFXMLRenderer(GenericRDFBaseRenderer):
    format = "rdf"
    media_type = "application/rdf+xml"
    rdflib_format = "xml"


class GenericRDFN3Renderer(GenericRDFBaseRenderer):
    format = "rdf"
    media_type = "text/n3"
    rdflib_format = "n3"


class CidocTTLRenderer(GenericRDFBaseRenderer):
    format = "cidoc"
    media_type = "text/ttl"
    rdflib_format = "ttl"


class CidocXMLRenderer(GenericRDFBaseRenderer):
    format = "cidoc"
    media_type = "application/rdf+xml"
    rdflib_format = "xml"
