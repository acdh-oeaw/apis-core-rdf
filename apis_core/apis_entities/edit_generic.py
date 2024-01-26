from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.shortcuts import redirect, get_object_or_404
from django.template.loader import get_template
from django.template.response import TemplateResponse
from django.urls import reverse
from django.utils.decorators import method_decorator
from django.views import View
from django.views.generic import DeleteView
from .forms import get_entities_form, GenericEntitiesStanbolForm
from .views import set_session_variables
from apis_core.utils import helpers
from apis_core.apis_entities.mixins import EntityMixin, EntityInstanceMixin
from apis_core.utils.helpers import get_member_for_entity


@method_decorator(login_required, name="dispatch")
class GenericEntitiesEditView(EntityInstanceMixin, View):
    def get(self, request, *args, **kwargs):
        request = set_session_variables(request)

        side_bar = helpers.triple_sidebar(self.pk, self.entity, request, detail=False)

        form = get_member_for_entity(self.entity_model, suffix="Form")
        if form is None:
            form = get_entities_form(self.entity.title())
        form = form(instance=self.instance)
        if "apis_bibsonomy" in settings.INSTALLED_APPS:
            apis_bibsonomy = getattr(settings, "APIS_BIBSONOMY_FIELDS", [])
            if isinstance(apis_bibsonomy, list):
                apis_bibsonomy = "|".join([x.strip() for x in apis_bibsonomy])
        else:
            apis_bibsonomy = False
        template = get_template("apis_entities/edit_generic.html")
        context = {
            "entity_type": self.entity,
            "form": form,
            "instance": self.instance,
            "right_card": side_bar,
            "apis_bibsonomy": apis_bibsonomy,
        }
        form_merge_with = GenericEntitiesStanbolForm(self.entity, ent_merge_pk=self.pk)
        context["form_merge_with"] = form_merge_with
        return HttpResponse(template.render(request=request, context=context))

    def post(self, request, *args, **kwargs):
        form = get_member_for_entity(self.entity_model, suffix="Form")
        if form is None:
            form = get_entities_form(self.entity.title())
        form = form(request.POST, instance=self.instance)
        if form.is_valid():
            form.save()
            return redirect(
                reverse(
                    "apis:apis_entities:generic_entities_edit_view",
                    kwargs={"pk": self.pk, "entity": self.entity},
                )
            )
        else:
            template = get_template("apis_entities/edit_generic.html")
            context = {
                "form": form,
                "entity_type": self.entity,
                "instance": self.instance,
            }
            if self.entity.lower() != "place":
                form_merge_with = GenericEntitiesStanbolForm(
                    self.entity, ent_merge_pk=self.pk
                )
                context["form_merge_with"] = form_merge_with
                return TemplateResponse(request, template, context=context)
            return HttpResponse(template.render(request=request, context=context))


@method_decorator(login_required, name="dispatch")
class GenericEntitiesCreateView(EntityMixin, View):
    def get(self, request, *args, **kwargs):
        form = get_member_for_entity(self.entity_model, suffix="Form")
        if form is None:
            form = get_entities_form(self.entity.title())
        form = form()
        permissions = {
            "create": request.user.has_perm("entities.add_{}".format(self.entity))
        }
        template = get_template("apis_entities/create_generic.html")
        return HttpResponse(
            template.render(
                request=request,
                context={
                    "entity_type": self.entity,
                    "permissions": permissions,
                    "form": form,
                },
            )
        )

    def post(self, request, *args, **kwargs):
        form = get_member_for_entity(self.entity_model, suffix="Form")
        if form is None:
            form = get_entities_form(self.entity.title())
        form = form(request.POST)
        if form.is_valid():
            entity_2 = form.save()
            return redirect(
                reverse(
                    "apis:apis_entities:generic_entities_detail_view",
                    kwargs={"pk": entity_2.pk, "entity": self.entity},
                )
            )
        else:
            permissions = {
                "create": request.user.has_perm(
                    "apis_entities.add_{}".format(self.entity)
                )
            }
            template = get_template("apis_entities/create_generic.html")
            return HttpResponse(
                template.render(
                    request=request,
                    context={
                        "permissions": permissions,
                        "form": form,
                    },
                )
            )


@method_decorator(login_required, name="dispatch")
class GenericEntitiesCreateStanbolView(EntityMixin, View):
    def post(self, request, *args, **kwargs):
        ent_merge_pk = kwargs.get("ent_merge_pk", False)
        if ent_merge_pk:
            form = GenericEntitiesStanbolForm(
                self.entity, request.POST, ent_merge_pk=ent_merge_pk
            )
        else:
            form = GenericEntitiesStanbolForm(self.entity, request.POST)
        # form = form(request.POST)
        if form.is_valid():
            entity_2 = form.save()
            if ent_merge_pk:
                entity_2.merge_with(int(ent_merge_pk))
            return redirect(
                reverse(
                    "apis:apis_entities:generic_entities_edit_view",
                    kwargs={"pk": entity_2.pk, "entity": self.entity},
                )
            )
        else:
            permissions = {
                "create": request.user.has_perm(
                    "apis_entities.add_{}".format(self.entity)
                )
            }
            template = get_template("apis_entities/create_generic.html")
            return HttpResponse(
                template.render(
                    request=request, context={"permissions": permissions, "form": form}
                )
            )


@method_decorator(login_required, name="dispatch")
class GenericEntitiesDeleteView(EntityInstanceMixin, DeleteView):
    template_name = getattr(
        settings, "APIS_DELETE_VIEW_TEMPLATE", "confirm_delete.html"
    )

    def get_queryset(self):
        return self.entity_model.objects.all()

    def dispatch(self, request, *args, **kwargs):
        self.success_url = reverse(
            "apis_core:apis_entities:generic_entities_list",
            kwargs={"entity": self.entity},
        )
        return super(GenericEntitiesDeleteView, self).dispatch(request, *args, **kwargs)


@method_decorator(login_required, name="dispatch")
class GenericEntitiesDuplicateView(EntityInstanceMixin, View):
    def get(self, request, *args, **kwargs):
        source_obj = get_object_or_404(self.entity_model, pk=self.pk)

        newobj = source_obj.duplicate()

        return redirect(
            reverse(
                "apis:apis_entities:generic_entities_edit_view",
                kwargs={"pk": newobj.id, "entity": self.entity},
            )
        )
