# SPDX-FileCopyrightText: 2023 Birger Schacht
# SPDX-License-Identifier: MIT

import re

from apis_core.utils.settings import dict_from_toml_directory


def clean_uri(uri: str) -> str:
    configs = dict_from_toml_directory("cleanuri")
    if uri is not None:
        for key, definition in configs.items():
            regex = definition["regex"]
            replace = definition["replace"]
            if m := re.match(regex, uri):
                uri = replace.format(m.group(1))
    return uri
