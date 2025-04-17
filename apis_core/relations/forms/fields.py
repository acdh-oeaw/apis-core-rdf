from django import forms
from django.urls import reverse

from apis_core.core.fields import ApisListSelect2
from apis_core.relations.utils import relation_content_types


def list_relation_choices():
    return [(rel.id, rel.model_class().name()) for rel in relation_content_types()]


class RelationMultiWidget(forms.MultiWidget):
    template_name = "relations/relation_multiwidget.html"
    use_fieldset = False

    def __init__(self, attrs=None):
        relation_choices = [(None, "---")] + list_relation_choices()
        widgets = [
            forms.widgets.Select(choices=relation_choices),
            ApisListSelect2(url=reverse("apis_core:apis_entities:autocomplete")),
        ]
        super().__init__(widgets)

    def decompress(self, value):
        return [value, value]


class RelationField(forms.MultiValueField):
    widget = RelationMultiWidget()

    def __init__(self, *args, **kwargs):
        fields = (forms.ChoiceField(choices=list_relation_choices()), forms.CharField())
        super().__init__(fields=fields, *args, **kwargs)

    def compress(self, data_list):
        return data_list
