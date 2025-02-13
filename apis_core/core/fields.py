from dal_select2.widgets import (
    ListSelect2,
    ModelSelect2,
    ModelSelect2Multiple,
    Select2,
    Select2Multiple,
    TagSelect2,
)


class ApisListSelect2(ListSelect2):
    autocomplete_function = "apis_select2"


class ApisModelSelect2(ModelSelect2):
    autocomplete_function = "apis_select2"


class ApisModelSelect2Multiple(ModelSelect2Multiple):
    autocomplete_function = "apis_select2"


class ApisSelect2(Select2):
    autocomplete_function = "apis_select2"


class ApisSelect2Multiple(Select2Multiple):
    autocomplete_function = "apis_select2"


class ApisTagSelect2(TagSelect2):
    autocomplete_function = "apis_select2"
