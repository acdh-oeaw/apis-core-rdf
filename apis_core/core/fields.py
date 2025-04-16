from dal_select2.widgets import (
    ListSelect2,
    ModelSelect2,
    ModelSelect2Multiple,
    Select2,
    Select2Multiple,
    TagSelect2,
)


class BootstrapAttrMixin:
    def build_attrs(self, *args, **kwargs):
        attrs = super().build_attrs(*args, **kwargs)
        attrs["data-theme"] = "bootstrap-5"
        return attrs


class ApisListSelect2(BootstrapAttrMixin, ListSelect2):
    autocomplete_function = "apis_select2"


class ApisModelSelect2(BootstrapAttrMixin, ModelSelect2):
    autocomplete_function = "apis_select2"


class ApisModelSelect2Multiple(BootstrapAttrMixin, ModelSelect2Multiple):
    autocomplete_function = "apis_select2"


class ApisSelect2(BootstrapAttrMixin, Select2):
    autocomplete_function = "apis_select2"


class ApisSelect2Multiple(BootstrapAttrMixin, Select2Multiple):
    autocomplete_function = "apis_select2"


class ApisTagSelect2(BootstrapAttrMixin, TagSelect2):
    autocomplete_function = "apis_select2"
