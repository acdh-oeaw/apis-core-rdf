from django import forms

from apis_core.apis_entities.widgets import PlaceLookup


class PlaceLookupField(forms.CharField):
    widget = PlaceLookup

    def __init__(
        self,
        *args,
        label_id="id_label",
        longitude_id="id_longitude",
        latitude_id="id_latitude",
        **kwargs,
    ):
        self.label_id = label_id
        self.longitude_id = longitude_id
        self.latitude_id = latitude_id
        super().__init__(*args, **kwargs)

    def widget_attrs(self, widget):
        attrs = super().widget_attrs(widget)
        attrs["data-label-id"] = self.label_id
        attrs["data-longitude-id"] = self.longitude_id
        attrs["data-latitude-id"] = self.latitude_id
        return attrs
