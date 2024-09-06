# SPDX-FileCopyrightText: 2023 Birger Schacht
# SPDX-License-Identifier: MIT

import importlib
import logging
import re
from typing import Tuple

from rdflib import Graph

from apis_core.utils.normalize import clean_uri
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
    uri = clean_uri(uri)
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
    model_attributes = dict()
    if matching_definition:
        attributes = matching_definition.get("attributes", [])
        sparql_attributes = list(filter(lambda d: d.get("sparql"), attributes))
        for attribute in sparql_attributes:
            result = graph.query(attribute["sparql"])
            for binding in result.bindings:
                # {rdflib.term.Variable('somekey'): rdflib.term.Literal('some value')}
                for key, value in binding.items():
                    model_attributes[str(key)] = str(value)
    else:
        raise AttributeError(f"No matching definition found for {uri}")
    return matching_definition, model_attributes
