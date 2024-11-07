from django import forms

from apis_core.relations.forms import RelationForm


class LivesInForm(RelationForm):
    # we add a big notes field to this relation, both to demonstrate how custom forms
    # work in APIS, but also to test for an overflow in the form
    notes = forms.CharField(widget=forms.Textarea(attrs={"rows": "70"}), required=False)
