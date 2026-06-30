from django.contrib.contenttypes.models import ContentType
from django.forms.widgets import Select, SelectMultiple
from django.urls import reverse_lazy


class AutocompleteSingleSelect(Select):
    template_name = "widgets/autocomplete_singleselect.html"

    class Media:
        css = {"all": ["css/widgets/autocomplete.css"]}

    def __init__(self, field, attrs=None):
        self.field = field
        super().__init__(attrs)

    def get_context(self, name, value, attrs):
        ctx = super().get_context(name, value, attrs)
        ct = ContentType.objects.get_for_model(self.field._queryset.model)
        ctx["widget"]["value"] = ""
        if value:
            ctx["widget"]["value"] = self.field._queryset.model.objects.get(pk=value)
        ctx["widget"]["url"] = (
            reverse_lazy("apis_core:generic:autocomplete-choices", args=[ct])
            + "?fieldname="
            + ctx["widget"]["name"]
        )
        return ctx


class AutocompleteMultiSelect(SelectMultiple):
    template_name = "widgets/autocomplete_multiselect.html"

    class Media:
        css = {
            "all": [
                "css/widgets/autocomplete.css",
                "css/widgets/autocomplete_multiselect.css",
            ]
        }

    def __init__(self, field, attrs=None):
        self.field = field
        super().__init__(attrs)

    def get_context(self, name, value, attrs):
        ctx = super().get_context(name, value, attrs)
        ct = ContentType.objects.get_for_model(self.field._queryset.model)
        ctx["widget"]["url"] = (
            reverse_lazy("apis_core:generic:autocomplete-choices", args=[ct])
            + "?fieldname="
            + ctx["widget"]["name"]
            + "&multiple"
        )
        ctx["widget"]["value"] = []
        if value:
            ctx["widget"]["value"] = self.field._queryset.model.objects.filter(
                pk__in=value
            )
        return ctx
