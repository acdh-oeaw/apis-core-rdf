# SPDX-FileCopyrightText: 2023 Birger Schacht
# SPDX-License-Identifier: MIT

import logging
import tomllib
from urllib.parse import urlparse

from django.conf import settings
from django.template.utils import get_app_template_dirs

logger = logging.getLogger(__name__)


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


def dict_from_toml_directory(directory: str) -> dict:
    configs = {}
    pathlists = [path.glob("**/*.toml") for path in get_app_template_dirs(directory)]
    for file in [path for pathlist in pathlists for path in pathlist]:
        try:
            configs[file.resolve()] = tomllib.loads(file.read_text())
        except Exception as e:
            logger.error(f"TOML parser could not read {file}: {e}")
    return configs


def internal_uris() -> list[str]:
    return set([apis_base_uri()] + getattr(settings, "APIS_FORMER_BASE_URIS", []))


def apis_base_uri() -> str:
    return getattr(settings, "APIS_BASE_URI", "https://example.org")


def rdf_namespace_prefix() -> str:
    if hasattr(settings, "APIS_RDF_NAMESPACE_PREFIX"):
        return settings.APIS_RDF_NAMESPACE_PREFIX
    base_uri = urlparse(apis_base_uri())
    return base_uri.hostname.split(".", 1)[0]
