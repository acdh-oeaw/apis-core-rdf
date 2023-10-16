# SPDX-FileCopyrightText: 2023 Birger Schacht
# SPDX-License-Identifier: MIT

from pathlib import Path
from django.conf import settings


def default_settings() -> Path:
    curpath = Path(__file__).parent
    return curpath.parent / "default_settings"


def clean_uri_mapping_file() -> Path:
    default = default_settings() / "URI_replace_settings.yml"
    mapping_file = getattr(settings, "CLEANURI_MAPPINGS", default)
    return Path(mapping_file)


def rdf_object_mapping_file() -> Path:
    default = default_settings() / "RDF_default_settings.toml"
    mapping_file = getattr(settings, "APIS_RDF_YAML_SETTINGS", default)
    return Path(mapping_file)


def get_entity_settings_by_modelname(entity: str = None) -> dict:
    """
    return the settings for a specific entity or the dict for all entities
    if no entity is given
    """
    apis_entities = getattr(settings, "APIS_ENTITIES", {})
    if entity:
        # lookup entity settings by name and by capitalized name
        return apis_entities.get(entity, apis_entities.get(entity.capitalize(), {}))
    return apis_entities


def list_links_to_edit() -> bool:
    return getattr(settings, "APIS_LIST_LINKS_TO_EDIT", False)
