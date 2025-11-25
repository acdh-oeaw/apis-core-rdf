import base64
import json
import logging
from urllib.parse import urlparse

import httpx
from django.template.loader import render_to_string

logger = logging.getLogger(__name__)


class ExternalAutocomplete:
    """
    This is a helper base class for implementing external
    autocomplete classes. <Modelname>ExernalAutocomplete classes
    are expected to have a `get_results(self, q)` method that
    returns a list of results usable by the autocomplete view.
    This base class implements this `get_results` method in a
    way that you can inherit from it and just define a list of
    `adapters`. Those adapters are then used one by one to
    add external autocomplete search results.
    """

    client = httpx.Client()
    adapters = []

    def get_results(self, q):
        results = []
        for adapter in self.adapters:
            results.extend(adapter.get_results(q, self.client))
        return results


class ExternalAutocompleteAdapter:
    """
    Base class for ExternalAutocompleteAdapters. It provides
    the methods used for templating the autocomplete results.
    You can pass a `template` name to initialization, which
    is then used to style the results.
    """

    template = None

    def __init__(self, *args, **kwargs):
        self.template = kwargs.get("template", None)
        self.data_mapping = kwargs.get("data_mapping", {})

    def _nested_get(self, dict_, keys):
        """
        Get a nested value from a dict by poviding the
        path as a list of keys
        """
        for index, key in enumerate(keys):
            if index == len(keys) - 1:
                return [dict_.get(key, "")]
            dict_ = dict_.get(key, {})

    def map_data(self, result) -> dict:
        """
        Map data from the result to a a new dict. The new dict
        is built using the settings in `.data_mapping`, which
        should be a mapping of keys to be created in the result
        dict to paths in the `result` item.
        """
        data = {}
        for key, val in self.data_mapping.items():
            if isinstance(val, str):
                val = [val]
            data[key] = self._nested_get(result, val)
        return data

    def add_data_to_uri(self, uri, data):
        b64_data = base64.b64encode(json.dumps(data).encode()).decode("ascii")
        if urlparse(uri).query:
            uri += f"&anero_ac_data={b64_data}"
        else:
            uri += f"?anero_ac_data={b64_data}"
        return uri

    def default_template(self, result):
        return f'{result["label"]} <a href="{result["id"]}">{result["id"]}</a>'

    def get_result_label(self, result):
        if self.template:
            return render_to_string(self.template, {"result": result})
        return self.default_template(result)


class TypeSenseAutocompleteAdapter(ExternalAutocompleteAdapter):
    """
    This autocomplete adapters queries typesense collections on a
    typesense server. The `collections` variable can either be a
    string or a list - if its a string, that collection is queried
    directly, if its a list, the adapter uses typesense `multi_search`
    endpoint.
    """

    collections = None
    token = None
    server = None

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.collections = kwargs.get("collections", None)
        self.token = kwargs.get("token", None)
        self.server = kwargs.get("server", None)

    def default_template(self, result):
        return super().default_template(result["document"])

    def extract(self, res):
        if res.get("document"):
            data = self.map_data(res)
            uri = self.add_data_to_uri(res["document"]["id"], data)
            return {
                "id": uri,
                "text": self.get_result_label(res),
                "selected_text": self.get_result_label(res),
            }
        logger.error(
            "Could not parse result from typesense collection %s: %s",
            self.collections,
            res,
        )
        return False

    def get_results(self, q, client=httpx.Client()):
        headers = {"X-TYPESENSE-API-KEY": self.token}
        res = None
        if self.token and self.server:
            match self.collections:
                # if there is only on collection configured, we hit that collection directly
                case str() as collection:
                    url = f"{self.server}/collections/{collection}/documents/search?q={q}&query_by=description&query_by=label"
                    res = client.get(url, headers=headers)
                # if there are multiple collections configured, we use the `multi_search` endpoint
                case list() as collectionlist:
                    url = f"{self.server}/multi_search?q={q}&query_by=description&query_by=label"
                    data = {"searches": []}
                    for collection in collectionlist:
                        data["searches"].append({"collection": collection})
                    res = client.post(url, data=json.dumps(data), headers=headers)
                case unknown:
                    logger.error("Don't know what to do with collection %s", unknown)

            if res:
                data = res.json()
                hits = data.get("hits", [])
                for result in data.get("results", []):
                    hits.extend(result["hits"])
                return list(filter(bool, map(self.extract, hits)))
        return []


class LobidAutocompleteAdapter(ExternalAutocompleteAdapter):
    """
    This autocomplete adapters queries the lobid autocomplete apis.
    See https://lobid.org/gnd/api for details
    You can pass a `lobid_params` dict which will then be use as GET
    request parameters.
    """

    params = {}

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.params = kwargs.get("params", {})

    def extract(self, res):
        data = self.map_data(res)
        uri = self.add_data_to_uri(res["id"], data)
        return {
            "id": uri,
            "text": self.get_result_label(res),
            "selected_text": self.get_result_label(res),
        }

    def get_results(self, q, client=httpx.Client()):
        endpoint = "https://lobid.org/gnd/search?"
        self.params["q"] = q
        res = client.get(endpoint, params=self.params)
        if res:
            return list(filter(bool, map(self.extract, res.json())))
        return []
