from django.views.generic.base import TemplateView

from apis_core.documentation.utils import Datamodel


class Documentation(TemplateView):
    template_name = "documentation.html"

    def get_context_data(self):
        ctx = super().get_context_data()
        ctx["datamodel"] = Datamodel()
        return ctx
