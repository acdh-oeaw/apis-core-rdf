from django.contrib.contenttypes.models import ContentType
from django.forms.widgets import Input
from django.urls import reverse_lazy


class Autocomplete(Input):
    template_name = "widgets/autocomplete.html"

    class Media:
        js = ["js/widgets/autocomplete.js"]
        css = {"all": ["css/widgets/autocomplete.css"]}

    def __init__(self, url: str, attrs=None):
        self.url = url
        super().__init__(attrs)

    def get_context(self, name, value, attrs):
        ctx = super().get_context(name, value, attrs)
        ctx["widget"]["url"] = self.url
        return ctx


class MultiSelect(Input):
    template_name = "widgets/multiselect.html"

    class Media:
        css = {"all": ["css/widgets/multiselect.css"]}

    def __init__(self, field, attrs=None):
        self.field = field
        super().__init__(attrs)

    def get_context(self, name, value, attrs):
        ctx = super().get_context(name, value, attrs)
        ct = ContentType.objects.get_for_model(self.field._queryset.model)
        ctx["widget"]["url"] = reverse_lazy(
            "apis_core:generic:autocomplete", args=[ct, ctx["widget"]["name"]]
        )
        ctx["widget"]["value"] = self.field._queryset.model.objects.filter(pk__in=value)
        return ctx
