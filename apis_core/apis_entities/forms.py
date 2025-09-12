from django.forms.fields import ChoiceField
from django.utils.translation import gettext_lazy as _

from apis_core.apis_entities.fields import PlaceLookupField
from apis_core.apis_entities.utils import get_feature_codes
from apis_core.generic.forms import GenericModelForm


class E53_PlaceForm(GenericModelForm):
    place = PlaceLookupField(
        required=False,
        label=_("Search places"),
        help_text=_("Click on a result to fill the form"),
    )
    feature_code = ChoiceField(choices=get_feature_codes, required=False)

    field_order = ["place"]
