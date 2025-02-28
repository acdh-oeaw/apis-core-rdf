from django import forms
from django.urls import reverse
from apis_core.core.fields import ApisListSelect2
from apis_core.relations.utils import relation_content_types


class RelationSelect(forms.MultiWidget):
    def __init__(self, attrs=None):
        relation_choices = [(rel.id, rel.model_class().name()) for rel in relation_content_types()]
        widgets = [
                forms.widgets.Select(choices=relation_choices),
                ApisListSelect2(url=reverse("apis_core:apis_entities:autocomplete")),
                ]
        super().__init__(widgets)

    def decompress(self, value):
        print(value)
        return [value, value]


class RelationField(forms.MultiValueField):
    widget = RelationSelect()

    def __init__(self, *args, **kwargs):
        relation_choices = [(rel.id, rel.model_class().name()) for rel in relation_content_types()]
        fields = (
            forms.ChoiceField(choices=relation_choices),
            forms.CharField()
        )
        #kwargs["widget"] = IncludeExcludeMultiWidget(widgets=[f.widget for f in fields])
        super().__init__(fields=fields, *args, **kwargs)

    def compress(self, data_list):
        print(f"{data_list=}")
        return data_list
