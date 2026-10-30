from django import forms
from django.apps import apps
from django.contrib.contenttypes.models import ContentType

from apis_core.relations.utils import relation_content_types
from apis_core.search.widgets import AutocompleteSingleSelect


def list_relation_choices(model=None):
    return [
        (rel.id, rel.model_class().name())
        for rel in relation_content_types(any_model=model)
    ]


class RelationMultiWidget(forms.MultiWidget):
    template_name = "relations/relation_multiwidget.html"
    use_fieldset = False

    def __init__(self, attrs=None, choices=[], model=None):
        relation_choices = [(None, "---")] + choices
        widgets = [
            forms.widgets.Select(choices=relation_choices),
        ]
        rels = relation_content_types(any_model=model)
        models = {r.model_class().subj_model for r in rels} | {
            r.model_class().obj_model for r in rels
        }
        content_types = [ContentType.objects.get_for_model(model) for model in models]
        if apps.is_installed("apis_core.search"):
            widgets.append(AutocompleteSingleSelect(content_types=content_types))
        else:
            widgets.append(
                forms.widgets.TextInput(
                    attrs={"disabled": "True", "value": "Search app is not active"}
                )
            )
        super().__init__(widgets)

    def decompress(self, value):
        return [value, value]


class RelationField(forms.MultiValueField):
    def __init__(self, model=None, *args, **kwargs):
        choices = list_relation_choices(model)
        self.widget = RelationMultiWidget(choices=choices, model=model)
        fields = (forms.ChoiceField(choices=choices), forms.CharField())
        super().__init__(fields=fields, *args, **kwargs)

    def compress(self, data_list):
        return data_list
