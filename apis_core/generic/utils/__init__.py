import base64
import json
import logging
from typing import Tuple
from urllib.parse import parse_qs, urlencode, urlparse, urlunparse

from AcdhArcheAssets.uri_norm_rules import get_normalized_uri

logger = logging.getLogger(__name__)


def get_autocomplete_data_and_normalized_uri(
    uri: str, key: str = "anero_ac_data"
) -> Tuple[dict, str]:
    urlparts = urlparse(uri)
    query = urlparts.query
    params = parse_qs(query)
    data = params.pop(key, {})
    if data:
        try:
            data = json.loads(base64.b64decode(data[0]))
        except Exception as e:
            logger.debug("Could not decode anero_ac_data: %s", e)
            data = {}
    urlparts = urlparts._replace(query=urlencode(params, doseq=True))
    uri = get_normalized_uri(urlunparse(urlparts))
    return data, uri
