# SPDX-FileCopyrightText: 2023 Birger Schacht
# SPDX-License-Identifier: MIT

import pathlib
import logging

from yaml import safe_load
from rdflib import Graph
from typing import Tuple

from apis_core.utils.settings import rdf_object_mapping_file
from apis_core.utils.normalize import clean_uri

logger = logging.getLogger(__name__)

definition_must_have_keys = ["filter_sparql", "model"]


def get_modelname_and_dict_from_uri(
    uri: str, settings_file: pathlib.Path = None
) -> Tuple[str, dict]:
    uri = clean_uri(uri)
    graph = Graph()
    graph.parse(uri)

    settings_file = settings_file or rdf_object_mapping_file()
    settings = safe_load(settings_file.read_text())
    matching_definition = None
    for key, definition in settings.items():
        if set(definition_must_have_keys) <= set(definition.keys()):
            if bool(graph.query(definition["filter_sparql"])):
                logger.info(f"Found {key} to match the Uri")
                matching_definition = definition
    model_attributes = dict()
    model_name = None
    if matching_definition:
        model_name = matching_definition.get("model")
        attributes = matching_definition.get("attributes", [])
        sparql_attributes = list(filter(lambda d: d.get("sparql"), attributes))
        for attribute in sparql_attributes:
            result = graph.query(attribute["sparql"])
            for binding in result.bindings:
                # {rdflib.term.Variable('somekey'): rdflib.term.Literal('some value')}
                for key, value in binding.items():
                    model_attributes[str(key)] = str(value)
    else:
        raise AttributeError("No matching definition found")
    return model_name, model_attributes
