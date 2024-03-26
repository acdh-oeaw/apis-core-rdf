from django.views.generic.base import TemplateView
from django.urls import reverse
from apis_core.generic.views import Create


class RelationForm(Create):

    def dispatch(self, request, *args, **kwargs):
        self.listonly = request.GET.get("listonly", "False") == "True"
        self.reverse = request.GET.get("reverse", "False") == "True"
        return super().dispatch(request, *args, **kwargs)

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs |= self.request.resolver_match.captured_kwargs
        kwargs["listonly"] = self.listonly
        kwargs["reverse"] = self.reverse
        return kwargs

    def get_success_url(self):
        ckwargs = self.request.resolver_match.captured_kwargs
        if self.listonly:
            return reverse("apis:relations_list", kwargs=ckwargs)
        return reverse("apis:generic:update", args=[ckwargs["fromcontenttype"], ckwargs["frompk"]])

    def form_invalid(self, form):
        print(form.cleaned_data)
        return super().form_invalid(form)


class RelationList(TemplateView):
    template_name = "relations/partials/relation_table.html"

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data()
        ctx["object"] = kwargs.get("fromcontenttype").model_class().objects.get(pk=kwargs.get("frompk"))
        ctx["tocontenttype"] = kwargs.get("tocontenttype")
        return ctx
