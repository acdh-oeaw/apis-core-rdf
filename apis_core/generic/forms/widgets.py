import json

from django.forms.widgets import Input


class NewlineSeparatedListWidget(Input):
    input_type = "text"
    template_name = "widgets/multiline.html"

    class Media:
        js = ["js/multiline.js"]

    def value_from_datadict(self, data, files, name):
        values = [item for item in data.getlist(name) if item]
        return "\n".join(values)

    def format_value(self, value):
        if value == "" or value is None:
            return None
        return value.split("\n")


class JSONListWidget(Input):
    input_type = "text"
    template_name = "widgets/multiline.html"

    class Media:
        js = ["js/multiline.js"]

    def value_from_datadict(self, data, files, name):
        values = [item for item in data.getlist(name) if item]
        return values

    def format_value(self, value):
        if value == "" or value is None:
            return None
        return json.loads(value)
