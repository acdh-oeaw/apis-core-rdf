import os

from apis_core.utils.autocomplete import (
    ExternalAutocomplete,
    LobidAutocompleteAdapter,
    TypeSenseAutocompleteAdapter,
)


class GroupExternalAutocomplete(ExternalAutocomplete):
    adapters = [
        LobidAutocompleteAdapter(
            params={
                "filter": "type:CorporateBody",
                "format": "json:preferredName,geographicAreaCode,dateOfEstablishment,broaderTermInstantial",
            }
        ),
    ]


class PlaceExternalAutocomplete(ExternalAutocomplete):
    adapters = [
        TypeSenseAutocompleteAdapter(
            collections=[
                "prosnet-wikidata-place-index",
                "prosnet-geonames-place-index",
            ],
            token=os.getenv("TYPESENSE_TOKEN", None),
            server=os.getenv("TYPESENSE_SERVER", None),
        ),
        LobidAutocompleteAdapter(
            params={
                "filter": "type:PlaceOrGeographicName",
                "format": "json:preferredName",
            }
        ),
    ]


class PersonExternalAutocomplete(ExternalAutocomplete):
    adapters = [
        TypeSenseAutocompleteAdapter(
            collections="prosnet-wikidata-person-index",
            token=os.getenv("TYPESENSE_TOKEN", None),
            server=os.getenv("TYPESENSE_SERVER", None),
        ),
        LobidAutocompleteAdapter(
            params={
                "filter": "type:Person",
                "format": "json:preferredName,professionOrOccupation",
            }
        ),
    ]
