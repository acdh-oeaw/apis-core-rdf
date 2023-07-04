import importlib

from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.contrib.contenttypes.models import ContentType
from django.db.models import Q
from django.http import HttpResponse
from django.shortcuts import redirect, get_object_or_404
from django.template.loader import get_template
from django.template.response import TemplateResponse
from django.urls import reverse
from django.utils.decorators import method_decorator
from django.views import View
from django.views.generic import DeleteView
from django_tables2 import RequestConfig
from reversion.models import Version

from apis_core.apis_labels.models import Label
from apis_core.apis_metainfo.models import Uri
from apis_core.apis_relations.models import TempTriple
from apis_core.apis_relations.tables import (
    get_generic_triple_table,
    LabelTableEdit,
)
from .forms import get_entities_form, GenericEntitiesStanbolForm
from .views import set_session_variables
from ..apis_vocabularies.models import TextType
from apis_core.utils import helpers
from apis_core.utils.settings import get_entity_settings_by_modelname
from apis_core.apis_entities.mixins import EntityMixin, EntityInstanceMixin
from apis_core.utils.helpers import get_member_for_entity


@method_decorator(login_required, name="dispatch")
class GenericEntitiesEditView(EntityInstanceMixin, View):
    def get(self, request, *args, **kwargs):
        request = set_session_variables(request)

        side_bar = []

        triples_related_all = (
            TempTriple.objects_inheritance.filter(
                Q(subj__pk=self.pk) | Q(obj__pk=self.pk)
            )
            .all()
            .select_subclasses()
        )

        for entity_class in helpers.get_classes_with_allowed_relation_from(self.entity):
            entity_content_type = ContentType.objects.get_for_model(entity_class)

            other_entity_class_name = entity_class.__name__.lower()

            triples_related_by_entity = triples_related_all.filter(
                (
                    Q(**{f"subj__self_contenttype": entity_content_type})
                    & Q(**{f"obj__pk": self.pk})
                )
                | (
                    Q(**{f"obj__self_contenttype": entity_content_type})
                    & Q(**{f"subj__pk": self.pk})
                )
            )

            table_class = get_generic_triple_table(
                other_entity_class_name=other_entity_class_name,
                entity_pk_self=self.pk,
                detail=False,
            )

            prefix = f"{other_entity_class_name}"
            title_card = prefix
            tb_object = table_class(data=triples_related_by_entity, prefix=prefix)
            tb_object_open = request.GET.get(prefix + "page", None)
            entity_settings = get_entity_settings_by_modelname(entity_class.__name__)
            per_page = entity_settings.get("relations_per_page", 10)
            RequestConfig(request, paginate={"per_page": per_page}).configure(tb_object)
            side_bar.append(
                # (title_card, tb_object, ''.join([x.title() for x in match]), tb_object_open)
                (
                    title_card,
                    tb_object,
                    f"triple_form_{self.entity}_to_{other_entity_class_name}",
                    tb_object_open,
                )
            )

        form = get_member_for_entity(self.entity_model, suffix="Form")
        if form is None:
            form = get_entities_form(self.entity.title())
        form = form(instance=self.instance)
        if "apis_bibsonomy" in settings.INSTALLED_APPS:
            apis_bibsonomy = getattr(settings, "APIS_BIBSONOMY_FIELDS", [])
            apis_bibsonomy_texts = getattr(settings, "APIS_BIBSONOMY_TEXTS", False)
            if apis_bibsonomy_texts:
                apis_bibsonomy.extend(
                    [
                        f"text_{self.pk}"
                        for pk in TextType.objects.filter(
                            name__in=apis_bibsonomy_texts
                        ).values_list("pk", flat=True)
                        if f"text_{self.pk}" not in apis_bibsonomy
                    ]
                )
            if isinstance(apis_bibsonomy, list):
                apis_bibsonomy = "|".join([x.strip() for x in apis_bibsonomy])
        else:
            apis_bibsonomy = False
        object_lod = Uri.objects.filter(root_object=self.instance)
        object_labels = Label.objects.filter(temp_entity__id=self.instance.id)
        tb_label = LabelTableEdit(
            data=object_labels, prefix=self.entity.title()[:2] + "L-"
        )
        tb_label_open = request.GET.get("PL-page", None)
        # side_bar.append(('Label', tb_label, 'PersonLabel', tb_label_open))
        RequestConfig(request, paginate={"per_page": 10}).configure(tb_label)
        template = get_template("apis_entities/edit_generic.html")
        context = {
            "entity_type": self.entity,
            "form": form,
            "instance": self.instance,
            "right_card": side_bar,
            "object_lod": object_lod,
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
            entity_2 = form.save()
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
    # model = ContentType.objects.get(
    #     app_label='apis_entities', model='tempentityclass').model_class()
    model = importlib.import_module("apis_core.apis_entities.models").TempEntityClass
    template_name = getattr(
        settings, "APIS_DELETE_VIEW_TEMPLATE", "confirm_delete.html"
    )

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
