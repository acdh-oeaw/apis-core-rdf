from django.utils.translation import gettext_lazy as _

from apis_core.apis_entities.fields import PlaceLookupField
from apis_core.generic.forms import GenericModelForm


class E53_PlaceForm(GenericModelForm):
    place = PlaceLookupField(
        required=False,
        label=_("Search places"),
        help_text=_("Click on a result to fill the form"),
    )
    field_order = ["place"]
