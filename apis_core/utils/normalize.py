# SPDX-FileCopyrightText: 2023 Birger Schacht
# SPDX-License-Identifier: MIT

import re
from apis_core.utils.settings import clean_uri_mapping_file
from yaml import safe_load


def clean_uri(uri: str) -> str:
    if uri:
        settings = safe_load(clean_uri_mapping_file().read_text())
        for mapping in settings.get("mappings", []):
            domain = mapping["domain"]
            regex = mapping["regex"]
            replace = mapping["replace"]
            if domain in uri:
                m = re.match(regex, uri)
                if m:
                    uri = replace.format(m.group(1))
    return uri
