from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.contrib.contenttypes.models import ContentType
from django.db.models import Q
from django.http import HttpResponse
from django.shortcuts import redirect, get_object_or_404, render
from django.template.loader import get_template, select_template
from django.template.response import TemplateResponse
from django.urls import reverse
from django.utils.decorators import method_decorator
from django.views import View
from django.views.generic import DeleteView
from django_tables2 import RequestConfig
from guardian.core import ObjectPermissionChecker
from reversion.models import Version
from django.template.loader import render_to_string
import importlib
from apis_core.apis_relations.models import Property, AbstractReification
from apis_core.apis_entities.models import AbstractEntity
from apis_core.apis_labels.models import Label
from apis_core.apis_metainfo.models import Uri
from apis_core.apis_relations.models import Triple, TempTriple
from apis_core.apis_relations.tables import LabelTableEdit, render_reification_table
from apis_core.apis_relations.forms import (
    render_reification_form_and_table,
    render_triple_form,
    render_triple_form_and_table,
)
from .forms import get_entities_form, FullTextForm, GenericEntitiesStanbolForm
from .views import get_highlighted_texts
from .views import set_session_variables
from ..apis_relations.views import ajax_2_load_triple_form, ajax_2_delete_reification
from ..apis_vocabularies.models import TextType
from apis_core.helper_functions import caching

if "apis_highlighter" in settings.INSTALLED_APPS:
    from apis_highlighter.forms import SelectAnnotatorAgreement


@method_decorator(login_required, name="dispatch")
class GenericEntitiesEditView(View):
    def get(self, request, *args, **kwargs):
        entity_self_type_str = kwargs["entity"]
        entity_self_id = kwargs["pk"]
        entity_self_class = caching.get_ontology_class_of_name(entity_self_type_str)
        entity_self_contenttype = caching.get_contenttype_of_class(entity_self_class)
        entity_self_instance = get_object_or_404(entity_self_class, pk=entity_self_id)
        request = set_session_variables(request)
        triple_pane = []
        # Iterate over all entity and reification classes for the relation view on the right pane
        for model_other_class in (
            caching.get_all_entity_classes() + caching.get_all_reification_classes()
        ):
            model_other_contenttype = caching.get_contenttype_of_class(
                model_other_class
            )
            model_other_class_str = model_other_class.__name__.lower()
            # check for allowed properties, then display only those classes where there properties
            allowed_property_list = Property.objects.filter(
                Q(subj_class=entity_self_contenttype, obj_class=model_other_contenttype)
                | Q(
                    subj_class=model_other_contenttype,
                    obj_class=entity_self_contenttype,
                )
            )
            if len(allowed_property_list) > 0:
                # if it's an entity class, load a simple triple form and table
                if issubclass(model_other_class, AbstractEntity):
                    relation_form = render_triple_form_and_table(
                        model_self_class_str=entity_self_type_str,
                        model_other_class_str=model_other_class_str,
                        model_self_id_str=str(entity_self_id),
                        request=request,
                    )
                # if it's a reification class, load the reification form and table
                elif issubclass(model_other_class, AbstractReification):
                    relation_form = render_reification_form_and_table(
                        model_self_class_str=entity_self_type_str,
                        reification_type_str=model_other_class_str,
                        model_self_id_str=str(entity_self_id),
                        request=request,
                    )
                # to be sure the surrounding code has not been wrongly modified
                else:
                    raise Exception("An invalid related entity class was passed")
                triple_pane.append(
                    {
                        "title": f"{model_other_class_str}",
                        "triple_form_and_table": relation_form,
                    }
                )
        # __before_rdf_refactoring__
        #
        # relations = AbstractRelation.get_relation_classes_of_entity_name(entity_name=entity)
        # side_bar = []
        # for rel in relations:
        #     match = [
        #         rel.get_related_entity_classA().__name__.lower(),
        #         rel.get_related_entity_classB().__name__.lower()
        #     ]
        #     prefix = "{}{}-".format(match[0].title()[:2], match[1].title()[:2])
        #     table = get_generic_relations_table(relation_class=rel, entity_instance=instance, detail=False)
        #     title_card = ''
        #     if match[0] == match[1]:
        #         title_card = entity.title()
        #         dict_1 = {'related_' + entity.lower() + 'A': instance}
        #         dict_2 = {'related_' + entity.lower() + 'B': instance}
        #         if 'apis_highlighter' in settings.INSTALLED_APPS:
        #             objects = rel.objects.filter_ann_proj(request=request).filter(
        #                 Q(**dict_1) | Q(**dict_2))
        #         else:
        #             objects = rel.objects.filter(
        #                 Q(**dict_1) | Q(**dict_2))
        #     else:
        #         if match[0].lower() == entity.lower():
        #             title_card = match[1].title()
        #         else:
        #             title_card = match[0].title()
        #         dict_1 = {'related_' + entity.lower(): instance}
        #         if 'apis_highlighter' in settings.INSTALLED_APPS:
        #             objects = rel.objects.filter_ann_proj(request=request).filter(**dict_1)
        #         else:
        #             objects = rel.objects.filter(**dict_1)
        #     tb_object = table(data=objects, prefix=prefix)
        #     tb_object_open = request.GET.get(prefix + 'page', None)
        #     RequestConfig(request, paginate={"per_page": 10}).configure(tb_object)
        #     side_bar.append((title_card, tb_object, ''.join([x.title() for x in match]), tb_object_open))
        form = get_entities_form(entity_self_type_str.title())
        form = form(instance=entity_self_instance)
        form_text = FullTextForm(
            entity=entity_self_type_str.title(), instance=entity_self_instance
        )
        if "apis_highlighter" in settings.INSTALLED_APPS:
            form_ann_agreement = SelectAnnotatorAgreement()
        else:
            form_ann_agreement = False
        if "apis_bibsonomy" in settings.INSTALLED_APPS:
            apis_bibsonomy = getattr(settings, "APIS_BIBSONOMY_FIELDS", [])
            apis_bibsonomy_texts = getattr(settings, "APIS_BIBSONOMY_TEXTS", False)
            if apis_bibsonomy_texts:
                apis_bibsonomy.extend(
                    [
                        f"text_{pk}"
                        for pk in TextType.objects.filter(
                            name__in=apis_bibsonomy_texts
                        ).values_list("pk", flat=True)
                        if f"text_{pk}" not in apis_bibsonomy
                    ]
                )
            if isinstance(apis_bibsonomy, list):
                apis_bibsonomy = "|".join([x.strip() for x in apis_bibsonomy])
        else:
            apis_bibsonomy = False
        object_revisions = Version.objects.get_for_object(entity_self_instance)
        object_lod = Uri.objects.filter(root_object=entity_self_instance)
        object_texts, ann_proj_form = get_highlighted_texts(
            request, entity_self_instance
        )
        object_labels = Label.objects.filter(temp_entity=entity_self_instance)
        tb_label = LabelTableEdit(
            data=object_labels, prefix=entity_self_type_str.title()[:2] + "L-"
        )
        tb_label_open = request.GET.get("PL-page", None)
        # side_bar.append(('Label', tb_label, 'PersonLabel', tb_label_open))
        RequestConfig(request, paginate={"per_page": 10}).configure(tb_label)
        perm = ObjectPermissionChecker(request.user)
        permissions = {
            "change": perm.has_perm(
                "change_{}".format(entity_self_type_str), entity_self_instance
            ),
            "delete": perm.has_perm(
                "delete_{}".format(entity_self_type_str), entity_self_instance
            ),
            "create": request.user.has_perm(
                "entities.add_{}".format(entity_self_type_str)
            ),
        }

        context = {
            "entity_type": entity_self_type_str,
            "form": form,
            "form_text": form_text,
            "instance": entity_self_instance,
            "triple_pane": triple_pane,
            "object_revisions": object_revisions,
            "object_texts": object_texts,
            "object_lod": object_lod,
            "ann_proj_form": ann_proj_form,
            "form_ann_agreement": form_ann_agreement,
            "apis_bibsonomy": apis_bibsonomy,
            "permissions": permissions,
        }
        form_merge_with = GenericEntitiesStanbolForm(
            entity_self_type_str, ent_merge_pk=entity_self_id
        )
        context["form_merge_with"] = form_merge_with

        return render(request, "apis_entities/edit_generic.html", context)

    def post(self, request, *args, **kwargs):
        entity = kwargs["entity"]
        pk = kwargs["pk"]
        entity_model = caching.get_ontology_class_of_name(entity)
        instance = get_object_or_404(entity_model, pk=pk)
        form = get_entities_form(entity.title())
        form = form(request.POST, instance=instance)
        form_text = FullTextForm(request.POST, entity=entity.title())
        if form.is_valid() and form_text.is_valid():
            entity_2 = form.save()
            form_text.save(entity_2)
            return redirect(
                reverse(
                    "apis:apis_entities:generic_entities_edit_view",
                    kwargs={"pk": pk, "entity": entity},
                )
            )
        else:
            template = get_template("apis_entities/edit_generic.html")
            perm = ObjectPermissionChecker(request.user)
            permissions = {
                "change": perm.has_perm("change_{}".format(entity), instance),
                "delete": perm.has_perm("delete_{}".format(entity), instance),
                "create": request.user.has_perm("entities.add_{}".format(entity)),
            }
            context = {
                "form": form,
                "entity_type": entity,
                "form_text": form_text,
                "instance": instance,
                "permissions": permissions,
            }
            if entity.lower() != "place":
                form_merge_with = GenericEntitiesStanbolForm(entity, ent_merge_pk=pk)
                context["form_merge_with"] = form_merge_with
                return TemplateResponse(request, template, context=context)
            return HttpResponse(template.render(request=request, context=context))


@method_decorator(login_required, name="dispatch")
class GenericEntitiesCreateView(View):
    def get(self, request, *args, **kwargs):
        entity = kwargs["entity"]
        form = get_entities_form(entity.title())
        form = form()
        form_text = FullTextForm(entity=entity.title())
        permissions = {
            "create": request.user.has_perm("entities.add_{}".format(entity))
        }
        template = get_template("apis_entities/edit_generic.html")
        entity_class = caching.get_ontology_class_of_name(entity)
        return HttpResponse(
            template.render(
                request=request,
                context={
                    "entity_type": entity,
                    "permissions": permissions,
                    "form": form,
                    "form_text": form_text,
                    "entity_verbose_name": entity_class._meta.verbose_name,
                },
            )
        )

    def post(self, request, *args, **kwargs):
        entity = kwargs["entity"]
        form = get_entities_form(entity.title())
        form = form(request.POST)
        form_text = FullTextForm(request.POST, entity=entity.title())
        if form.is_valid() and form_text.is_valid():
            entity_2 = form.save()
            form_text.save(entity_2)
            return redirect(
                reverse(
                    "apis:apis_entities:generic_entities_edit_view",
                    kwargs={"pk": entity_2.pk, "entity": entity},
                )
            )
        else:
            permissions = {
                "create": request.user.has_perm("apis_entities.add_{}".format(entity))
            }
            template = get_template("apis_entities/edit_generic.html")
            return HttpResponse(
                template.render(
                    request=request,
                    context={
                        "permissions": permissions,
                        "form": form,
                        "form_text": form_text,
                    },
                )
            )


@method_decorator(login_required, name="dispatch")
class GenericEntitiesCreateStanbolView(View):
    def post(self, request, *args, **kwargs):
        entity = kwargs["entity"]
        ent_merge_pk = kwargs.get("ent_merge_pk", False)
        if ent_merge_pk:
            form = GenericEntitiesStanbolForm(
                entity, request.POST, ent_merge_pk=ent_merge_pk
            )
        else:
            form = GenericEntitiesStanbolForm(entity, request.POST)
        # form = form(request.POST)
        if form.is_valid():
            entity_2 = form.save()
            if ent_merge_pk:
                entity_2.merge_with(int(ent_merge_pk))
            return redirect(
                reverse(
                    "apis:apis_entities:generic_entities_edit_view",
                    kwargs={"pk": entity_2.pk, "entity": entity},
                )
            )
        else:
            permissions = {
                "create": request.user.has_perm("apis_entities.add_{}".format(entity))
            }
            template = get_template("apis_entities/edit_generic.html")
            return HttpResponse(
                template.render(
                    request=request, context={"permissions": permissions, "form": form}
                )
            )


@method_decorator(login_required, name="dispatch")
class GenericEntitiesDeleteView(DeleteView):
    # model = ContentType.objects.get(
    #     app_label='apis_entities', model='tempentityclass').model_class()
    model = importlib.import_module("apis_core.apis_entities.models").TempEntityClass
    template_name = getattr(
        settings, "APIS_DELETE_VIEW_TEMPLATE", "apis_entities/confirm_delete.html"
    )

    def dispatch(self, request, *args, **kwargs):
        entity = kwargs["entity"]
        self.success_url = reverse(
            "apis_core:apis_entities:generic_entities_list", kwargs={"entity": entity}
        )
        return super(GenericEntitiesDeleteView, self).dispatch(request, *args, **kwargs)
