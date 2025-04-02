# SPDX-FileCopyrightText: 2025 Birger Schacht
# SPDX-License-Identifier: MIT

import logging
import tomllib
from collections import defaultdict
from pathlib import Path

from AcdhArcheAssets.uri_norm_rules import get_normalized_uri
from django.apps import apps
from rdflib import RDF, BNode, Graph, URIRef

logger = logging.getLogger(__name__)


def resolve(obj, graph):
    """
    Look at the value of object and return the parsed
    value. If the value starts and ens with angle brackets,
    we interpret it as and transform it to an URI.
    If the value is simple text we interpret it as an curie
    and we expand it using the graphs namespace manager.
    Otherwise we simply return the value
    """
    if obj.startswith("<") and obj.endswith(">"):
        return URIRef(obj[1:-1])
    if isinstance(obj, str):
        return graph.namespace_manager.expand_curie(obj)
    return obj


def find_matching_config(graph: Graph, models: list | None = None) -> dict | None:
    models = models or apps.get_models()
    models_with_config = [model for model in models if hasattr(model, "rdf_configs")]
    for model in models_with_config:
        for path in model.rdf_configs():
            config = tomllib.loads(Path(path).read_text())
            for _filter in config.get("filters", []):
                try:
                    triples = []
                    for predicate, obj in _filter.items():
                        triples.append(
                            (None, resolve(predicate, graph), resolve(obj, graph))
                        )
                    triples = [triple in graph for triple in triples]
                    if all(triples):
                        logger.debug("Using %s for parsing graph", path)
                        config["model"] = model
                        return config
                except ValueError:
                    logger.debug("Filter %s does not match", _filter)
    return None


def build_sparql_query(curie: str) -> str:
    """
    Build a SPARQL query with language preferences.

    Args:
        curie: predicate to filter on as defined in the toml.
                needs to include the predicate and optionally
                a lang tag to filter for separated with a comma.
                Eg "wdt:P122,en".

    Returns:
        A SPARQL query string
    """
    if curie.lower().strip().startswith(("select", "prefix")):
        return curie
    lang_tag = ""
    if "," in curie:
        curie, lang_tag = curie.split(",", 1)
        lang_tag = f'FILTER LANGMATCHES(LANG(?object), "{lang_tag}")'
    query = f"""
            SELECT ?object 
            WHERE {{ 
                ?subject {curie} ?object {lang_tag}
            }}
        """

    logger.debug("Generated SPARQL query: %s", query)
    return query


def get_value_graph(graph: Graph, curies: str | list[str]) -> list:
    values = []
    if isinstance(curies, str):
        curies = [curies]
    for curie in curies:
        results = graph.query(build_sparql_query(curie))
        objects = [result[0] for result in results]
        for obj in objects:
            if isinstance(obj, BNode):
                values.extend(
                    [
                        str(value)
                        for value in graph.objects(subject=obj)
                        if value != RDF.Seq
                    ]
                )
            else:
                values.append(str(obj))
    return list(dict.fromkeys(values))


def get_something_from_uri(uri: str, models: list | None = None) -> dict | None:
    uri = get_normalized_uri(uri)
    graph = Graph()
    graph.parse(uri)

    if config := find_matching_config(graph, models):
        result = defaultdict(list)
        result["model"] = config["model"]
        result["relations"] = defaultdict(list)

        for attribute, curies in config.get("attributes", {}).items():
            values = get_value_graph(graph, curies)
            result[attribute].extend(values)
        for relation, details in config.get("relations", {}).items():
            details["curies"] = get_value_graph(graph, details.get("curies", []))
            result["relations"][relation] = details
        return dict(result)
    return None
