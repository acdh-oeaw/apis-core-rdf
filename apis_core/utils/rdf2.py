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
                triples = [
                    (
                        None,
                        graph.namespace_manager.expand_curie(predicate),
                        graph.namespace_manager.expand_curie(obj),
                    )
                    for predicate, obj in _filter.items()
                ]
                triples = [triple in graph for triple in triples]
                if all(triples):
                    logger.debug("Using %s for parsing graph", path)
                    config["model"] = model
                    return config
    return None


def get_something_from_uri(uri: str) -> dict | None:
    uri = get_normalized_uri(uri)
    graph = Graph()
    graph.parse(uri)

    if config := find_matching_config(graph):
        result = defaultdict(list)
        result["model"] = config["model"]
        result["relations"] = defaultdict(list)

        for attribute, curies in config.get("attributes", {}).items():
            if isinstance(curies, str):
                curies = [curies]
            for curie in curies:
                values = []
                results = graph.query(
                    "SELECT ?object WHERE { ?subject " + curie + " ?object }"
                )
                objects = [result.object for result in results]
                for obj in objects:
                    if isinstance(obj, BNode):
                        values.extend(
                            [
                                value.toPython()
                                for value in graph.objects(subject=obj)
                                if value != RDF.Seq
                            ]
                        )
                    else:
                        values.append(obj.toPython())

                if attribute == "relations":
                    result["relations"][curie].extend(values)
                else:
                    result[attribute].extend(values)
        return dict(result)
    return None
