from django.forms import ModelForm
from apis_core.apis_relations.models import Triple, Property
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit, Layout, Row, Column


class TripleForm(ModelForm):
    class Meta:
        model = Triple
        exclude = ["subj"]

    def __init__(self, instance, entity_contenttype, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["obj"].queryset = entity_contenttype.model_class().objects.all()
        self.fields["obj"].label = entity_contenttype.model_class()._meta.label.split(
            "."
        )[1]

        direct_properties = Property.objects.filter(
            obj_class=entity_contenttype, subj_class=instance.self_contenttype
        )
        reverse_properties = Property.objects.filter(
            subj_class=entity_contenttype, obj_class=instance.self_contenttype
        )
        dp = direct_properties.values_list("id", "name_forward")
        rp = reverse_properties.values_list("id", "name_reverse")

        self.fields["prop"].choices = list(dp) + list(rp)

        self.helper = FormHelper(self)
        self.helper.layout = Layout(
            Row(
                Column("prop", css_class="col"),
                Column("obj", css_class="col"),
            )
        )
        self.helper.add_input(Submit("submit", "Submit", css_class="btn-primary"))
