from django.forms.widgets import Select

from .models import SearchEntry


class AutocompleteSingleSelect(Select):
    template_name = "search/widgets/autocomplete_singleselect.html"

    class Media:
        css = {"all": ["css/search/autocomplete-widget.css"]}

    def __init__(self, content_types=[], attrs=None):
        self.content_types = content_types
        super().__init__(attrs)

    def format_value(self, value):
        if value and "_" in value:
            content_type_id, object_id = value.split("_")
            return SearchEntry.objects.get(
                content_type_id=content_type_id, object_id=object_id
            ).title
        return value

    def get_context(self, name, value, attrs):
        ctx = super().get_context(name, value, attrs)
        ctx["widget"]["content_types"] = self.content_types
        return ctx
