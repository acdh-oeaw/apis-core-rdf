import urllib.parse
from django.urls import reverse
from django.contrib.contenttypes.models import ContentType

from apis_core.generic.forms import GenericModelForm


class RelationForm(GenericModelForm):

    def __init__(self, *args, **kwargs):
        print(kwargs)
        fromcontenttype = kwargs.pop("fromcontenttype", None)
        frompk = kwargs.pop("frompk", None)
        tocontenttype = kwargs.pop("tocontenttype", None)
        listonly = kwargs.pop("listonly", False)
        relreverse = kwargs.pop("reverse", False)

        super().__init__(*args, **kwargs)

        subj, obj = "subj", "obj"
        if relreverse:
            subj, obj = "obj", "subj"

        if fromcontenttype:
            self.fields[subj].label = fromcontenttype.name + " " + subj
        if fromcontenttype and frompk:
            self.fields[subj].disabled = True
            self.fields[subj].initial = fromcontenttype.model_class().objects.get(pk=frompk)
            self.fields[subj].widget = self.fields[subj].hidden_widget()
        if tocontenttype:
            self.fields[obj].widget.url = reverse("apis:generic:autocomplete", args=[tocontenttype])
            self.fields[obj].label = tocontenttype.name + " " + obj

        content_type = ContentType.objects.get_for_model(self.Meta.model)
        url = reverse("apis:relationform", args=[content_type, fromcontenttype, frompk, tocontenttype])
        params = {"reverse": relreverse, "listonly": listonly}
        self.helper.form_action = url + "?" + urllib.parse.urlencode(params)
        if listonly:
            self.helper.attrs = {"hx-post": self.helper.form_action, "hx-swap": "none"}
