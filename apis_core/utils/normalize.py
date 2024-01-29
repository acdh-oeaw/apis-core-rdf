# SPDX-FileCopyrightText: 2023 Birger Schacht
# SPDX-License-Identifier: MIT

import re
import tomllib
from apis_core.utils.settings import clean_uri_mapping_file


def clean_uri(uri: str) -> str:
    settings = tomllib.loads(clean_uri_mapping_file().read_text())
    if uri is not None:
        for entry in settings.values():
            regex = entry["regex"]
            replace = entry["replace"]
            if m := re.match(regex, uri):
                uri = replace.format(m.group(1))
    return uri
