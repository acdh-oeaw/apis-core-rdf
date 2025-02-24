# SPDX-FileCopyrightText: 2025 Birger Schacht
# SPDX-License-Identifier: MIT

import logging
from collections import defaultdict
from pathlib import Path

import tomllib
from AcdhArcheAssets.uri_norm_rules import get_normalized_uri
from django.apps import apps
from rdflib import RDF, BNode, Graph

logger = logging.getLogger(__name__)


def find_matching_config(graph: Graph) -> dict | None:
    models_with_config = [
        model for model in apps.get_models() if hasattr(model, "rdf_configs")
    ]
    for model in models_with_config:
        for path in model.rdf_configs():
            config = tomllib.loads(Path(path).read_text())
            for _filter in config.get("filters", []):
                try:
                    triples = []
                    for predicate, obj in _filter.items():
                        predicate = graph.namespace_manager.expand_curie(predicate)
                        match obj:
                            case str():
                                obj = graph.namespace_manager.expand_curie(obj)
                            case True:
                                obj = None
                        triples.append((None, predicate, obj))
                    triples = [triple in graph for triple in triples]
                    if all(triples):
                        logger.debug("Using %s for parsing graph", path)
                        config["model"] = model
                        return config
                except ValueError:
                    logger.debug("Filter %s does not match", _filter)
    return None


def get_value_graph(graph: Graph, curies: str | list[str]) -> list:
    values = []
    if isinstance(curies, str):
        curies = [curies]
    for curie in curies:
        if curie.startswith("SELECT "):
            results = graph.query(curie)
        else:
            results = graph.query(
                "SELECT ?object WHERE { ?subject " + curie + " ?object }"
            )
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


def get_something_from_uri(uri: str) -> dict | None:
    uri = get_normalized_uri(uri)
    graph = Graph()
    graph.parse(uri)

    if config := find_matching_config(graph):
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
