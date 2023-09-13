from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.contrib.contenttypes.models import ContentType
from django.forms import modelform_factory
from django.urls import reverse
from django.http import Http404, HttpResponse

from .models import Relation
from .forms import RelationForm
from .utils import relation_content_types
from .templatetags import relations


################################################
# Views working with a specific Relation type: #
################################################


class RelationView(CreateView):
    contenttype = None
    frominstance = None
    inverted = False
    partial = False
    template_name = "relations/list.html"
    tocontenttype = None

    def dispatch(self, request, *args, **kwargs):
        if contenttype := kwargs.get("contenttype"):
            self.contenttype = ContentType.objects.get_for_id(contenttype)
            if self.contenttype not in relation_content_types():
                raise Http404(
                    f"Relation with id {kwargs['contenttype']} does not exist"
                )
        if fromoid := self.kwargs.get("fromoid"):
            if fromcontenttype := self.kwargs.get("fromcontenttype"):
                self.frominstance = ContentType.objects.get_for_id(
                    fromcontenttype
                ).get_object_for_this_type(pk=fromoid)
        if tocontenttype := self.kwargs.get("tocontenttype"):
            self.tocontenttype = ContentType.objects.get_for_id(tocontenttype)
        if "partial" in self.request.GET:
            self.template_name = "relations/partial.html"
            self.partial = True
        return super().dispatch(request, *args, **kwargs)

    def get_form_class(self):
        model_class = Relation
        if self.contenttype:
            model_class = self.contenttype.model_class()
        return modelform_factory(model_class, form=RelationForm, exclude=[])

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()

        kwargs["frominstance"] = self.frominstance
        kwargs["tocontenttype"] = self.tocontenttype
        kwargs["inverted"] = self.inverted
        return kwargs

    def get_success_url(self):
        url = reverse("relation", kwargs=self.request.resolver_match.kwargs)
        if self.inverted:
            url = reverse("relationinverted", kwargs=self.request.resolver_match.kwargs)
        if self.partial:
            url += "?partial"
        return url

    def get_context_data(self, *args, **kwargs):
        ctx = super().get_context_data()
        if self.contenttype:
            ctx["model"] = self.contenttype.model_class()
        if "formonly" in self.request.GET:
            return ctx
        if "tableonly" in self.request.GET:
            ctx["form"] = None
        # if we are not working with a specific relation
        # there is no need to present a form:
        if not self.contenttype:
            ctx["form"] = None

        if tocontenttype := self.kwargs.get("tocontenttype"):
            tocontenttype = ContentType.objects.get_for_id(tocontenttype)
        ctx["table"] = relations.relations_table(
            relationtype=self.contenttype,
            instance=self.frominstance,
            tocontenttype=tocontenttype,
        )
        return ctx


#################################################
# Views working with single Relation instances: #
#################################################


class RelationUpdate(UpdateView):
    template_name = "relations/list.html"

    def get_object(self):
        return Relation.objects.get_subclass(id=self.kwargs["pk"])

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs["embedded"] = False
        return kwargs

    def get_form_class(self):
        return modelform_factory(type(self.get_object()), form=RelationForm, exclude=[])

    def get_success_url(self):
        return reverse(
            "relationupdate",
            args=[
                self.get_object().id,
            ],
        )


class RelationDelete(DeleteView):
    template_name = "confirm_delete.html"

    def delete(self, request, *args, **kwargs):
        res = super().delete(request, args, kwargs)
        if "status_only" in self.request.GET:
            return HttpResponse()
        return res

    def get_object(self):
        return Relation.objects.get_subclass(id=self.kwargs["pk"])

    def get_success_url(self):
        if self.request.GET.get("next"):
            return self.request.GET.get("next")
        contenttype = ContentType.objects.get_for_model(self.get_object())
        return reverse(
            "relation",
            args=[
                contenttype.id,
            ],
        )
