# SPDX-FileCopyrightText: 2023 Birger Schacht
# SPDX-License-Identifier: MIT

import importlib
import logging
import re
from collections import defaultdict
from pathlib import Path
from typing import Tuple

import tomllib
from AcdhArcheAssets.uri_norm_rules import get_normalized_uri
from django.apps import apps
from rdflib import RDF, BNode, Graph

from apis_core.utils.settings import dict_from_toml_directory

logger = logging.getLogger(__name__)


def definition_matches_model(definition: str, model: object) -> bool:
    if definition.get("superclass", False) and model:
        try:
            module, cls = definition.get("superclass").rsplit(".", 1)
            module = importlib.import_module(module)
            parent = getattr(module, cls)
            if issubclass(type(model), parent) or issubclass(model, parent):
                return True
        except Exception as e:
            logger.error("superclass %s led to: %s", definition.get("superclass"), e)
    return False


def definition_matches_uri(definition: str, uri: str) -> bool:
    if regex := definition.get("regex", False):
        logger.info("found regex %s", regex)
        pattern = re.compile(regex)
        if pattern.fullmatch(uri) is None:
            return False
    return True


def get_definition_and_attributes_from_uri(
    uri: str, model: object
) -> Tuple[dict, dict]:
    """
    This function looks for `.toml` files in the `rdfimport` app directories
    and loads all the files it can parse. For every file that contains a
    `superclass` key it checks if it is a superclass of `model`.
    It uses the first file that
    matches to extract attributes from the RDF endpoint and then returns both
    the parsed file contents and the extracted attributes.
    The reason we are also returning the parsed file contents is, that you then
    can define a model *in* the file and then use this function to iterate over
    a list of URIs and you can use the matched definition to choose which model
    to create.
    The dict containing the parsed file contents also contains the filename, to
    make debugging a bit easier.
    """
    uri = get_normalized_uri(uri)
    graph = Graph()
    graph.parse(uri)

    configs = dict_from_toml_directory("rdfimport")
    matching_definition = None
    for key, definition in configs.items():
        if definition_matches_model(definition, model) and definition_matches_uri(
            definition, uri
        ):
            matching_definition = definition
            matching_definition["filename"] = str(key)
            break
    model_attributes = defaultdict(list)
    if matching_definition:
        attributes = matching_definition.get("attributes", [])
        sparql_attributes = list(filter(lambda d: d.get("sparql"), attributes))
        for attribute in sparql_attributes:
            result = graph.query(attribute["sparql"])
            for binding in result.bindings:
                # {rdflib.term.Variable('somekey'): rdflib.term.Literal('some value')}
                for key, value in binding.items():
                    model_attributes[str(key)].append(str(value))
    else:
        raise AttributeError(f"No matching definition found for {uri}")
    return matching_definition, model_attributes


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
