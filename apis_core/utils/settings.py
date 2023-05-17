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
    default = default_settings() / "RDF_default_settings.yml"
    mapping_file = getattr(settings, "APIS_RDF_YAML_SETTINGS", default)
    return Path(mapping_file)
