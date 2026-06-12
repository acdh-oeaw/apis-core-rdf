from django.forms.widgets import Input


class PlaceLookup(Input):
    template_name = "entities/widgets/placelookup.html"

    class Media:
        js = ["js/placelookup.js"]
