from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.contrib.contenttypes.models import ContentType
from django.db.models import Q
from django.http import HttpResponse
from django.shortcuts import redirect, get_object_or_404, render
from django.template.loader import get_template
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

from apis_core.apis_entities.models import AbstractEntity
from apis_core.apis_labels.models import Label
from apis_core.apis_metainfo.models import Uri
from apis_core.apis_relations.models import Triple, TempTriple
from apis_core.apis_relations.tables import get_generic_relations_table, get_generic_triple_table, \
    LabelTableEdit, render_reification_table
from .forms import get_entities_form, FullTextForm, GenericEntitiesStanbolForm, \
    render_single_autocomplete_form_property, render_single_autocomplete_form_entity_OLD, create_contextual_triple_form_class, render_reification_form
from .views import get_highlighted_texts
from .views import set_session_variables
from ..apis_relations.views import ajax_2_load_contextual_triple_form, ajax_2_delete_reification
from ..apis_vocabularies.models import TextType

if 'apis_highlighter' in settings.INSTALLED_APPS:
    from apis_highlighter.forms import SelectAnnotatorAgreement


@method_decorator(login_required, name='dispatch')
class GenericEntitiesEditView(View):

    def get(self, request, *args, **kwargs):
        entity = kwargs['entity']
        pk = kwargs['pk']
        entity_model = AbstractEntity.get_entity_class_of_name(entity)
        instance = get_object_or_404(entity_model, pk=pk)
        request = set_session_variables(request)

        side_bar = []

        triples_related_all = TempTriple.objects_inheritance.filter(Q(subj__pk=pk) | Q(obj__pk=pk)).all().select_subclasses()

        for entity_class in AbstractEntity.get_all_entity_classes():

            # TODO __sresch__ : change this db fetch with the cached one from master
            entity_content_type = ContentType.objects.get_for_model(entity_class)

            other_entity_class_name = entity_class.__name__.lower()

            # TODO __sresch__ : Check if this filter call results in additional db hits
            triples_related_by_entity = triples_related_all.filter(
                (
                    Q(**{f"subj__self_content_type": entity_content_type}) & Q(**{f"obj__pk": pk})
                )
                | (
                    Q(**{f"obj__self_content_type": entity_content_type}) & Q(**{f"subj__pk": pk})
                )
            )

            table_class = get_generic_triple_table(other_entity_class_name=other_entity_class_name, entity_pk_self=pk, detail=False)

            prefix = f"{other_entity_class_name}"
            title_card = prefix
            tb_object = table_class(data=triples_related_by_entity, prefix=prefix)
            tb_object_open = request.GET.get(prefix + 'page', None)
            RequestConfig(request, paginate={"per_page": 10}).configure(tb_object)
            side_bar.append(
                # (title_card, tb_object, ''.join([x.title() for x in match]), tb_object_open)
                (title_card, tb_object, f"triple_form_{entity}_to_{other_entity_class_name}", tb_object_open)
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

        form = get_entities_form(entity.title())
        form = form(instance=instance)
        form_text = FullTextForm(entity=entity.title(), instance=instance)
        if 'apis_highlighter' in settings.INSTALLED_APPS:
            form_ann_agreement = SelectAnnotatorAgreement()
        else:
            form_ann_agreement = False
        if 'apis_bibsonomy' in settings.INSTALLED_APPS:
            apis_bibsonomy = getattr(settings, 'APIS_BIBSONOMY_FIELDS', [])
            apis_bibsonomy_texts = getattr(settings, "APIS_BIBSONOMY_TEXTS", False)
            if apis_bibsonomy_texts:
                apis_bibsonomy.extend([f"text_{pk}" for pk in TextType.objects.filter(name__in=apis_bibsonomy_texts).values_list('pk', flat=True) if f"text_{pk}" not in apis_bibsonomy])
            if isinstance(apis_bibsonomy, list):
                apis_bibsonomy = '|'.join([x.strip() for x in apis_bibsonomy])
        else:
            apis_bibsonomy = False
        object_revisions = Version.objects.get_for_object(instance)
        object_lod = Uri.objects.filter(root_object=instance)
        object_texts, ann_proj_form = get_highlighted_texts(request, instance)
        object_labels = Label.objects.filter(temp_entity=instance)
        tb_label = LabelTableEdit(data=object_labels, prefix=entity.title()[:2] + 'L-')
        tb_label_open = request.GET.get('PL-page', None)
        # side_bar.append(('Label', tb_label, 'PersonLabel', tb_label_open))
        RequestConfig(request, paginate={"per_page": 10}).configure(tb_label)
        perm = ObjectPermissionChecker(request.user)
        permissions = {'change': perm.has_perm('change_{}'.format(entity), instance),
                       'delete': perm.has_perm('delete_{}'.format(entity), instance),
                       'create': request.user.has_perm('entities.add_{}'.format(entity))}
        
        from apis_core.apis_entities.forms import VocabTable, VocabForm, GenericTripleForm2, PropertyAutocompleteFormField, EntityAutocompleteFormField
        from apis_core.apis_entities.autocomplete3 import GenericEntitiesAutocomplete
        from apis_core.apis_relations.tables import GenericTripleTable, ReificationTable
        from apis_ontology.models import E55_Type, BookPublicationRelationship
        context = {
            'entity_type': entity,
            'form': form,
            "table_xyz": GenericTripleTable(Triple.objects.all()),
            # "reification_table": ReificationTable(),
            'form_text': form_text,
            'instance': instance,
            'right_card': side_bar,
            'object_revisions': object_revisions,
            'object_texts': object_texts,
            'object_lod': object_lod,
            'ann_proj_form': ann_proj_form,
            'form_ann_agreement': form_ann_agreement,
            'apis_bibsonomy': apis_bibsonomy,
            'permissions': permissions}
        form_merge_with = GenericEntitiesStanbolForm(entity, ent_merge_pk=pk)
        context['form_merge_with'] = form_merge_with
        # template = get_template('apis_entities/entity_create_generic.html')
        # return HttpResponse(get_template("apis_entities/entity_create_generic.html").render(request=request, context=context))
        # form_xyz = GenericTripleForm2()
        # context["form_xyz"] = render_to_string(template_name=form_xyz.template_name, context={"form_xyz": form_xyz})

        # property_autocomplete_field_to_reif = PropertyAutocompleteFormField(
        #     entity_type_self_str="f10_person",
        #     entity_type_other_str="bookpublicationrelationship",
        #     field_id="custom_property_to_reif",
        # )
        # property_autocomplete_field_to_reif_rendered = render_to_string(
        #     property_autocomplete_field_to_reif.template_name,
        #     context={
        #         "property_autocomplete_field": property_autocomplete_field_to_reif,
        #         "id_form_field": "id_custom_property_to_reif",
        #         "autocomplete_url": "/apis/relations/autocomplete/f10_person/bookpublicationrelationship/",
        #     }
        # )
        # property_autocomplete_field_from_reif = PropertyAutocompleteFormField(
        #     entity_type_self_str="bookpublicationrelationship",
        #     entity_type_other_str="e40_legal_body",
        #     field_id="custom_property_from_reif",
        # )
        # property_autocomplete_field_from_reif_rendered = render_to_string(
        #     property_autocomplete_field_from_reif.template_name,
        #     context={
        #         "property_autocomplete_field": property_autocomplete_field_from_reif,
        #         "id_form_field": "id_custom_property_from_reif",
        #         "autocomplete_url": "/apis/relations/autocomplete/bookpublicationrelationship/e40_legal_body/",
        #     }
        # )
        # entity_autocomplete_field_from_reif = EntityAutocompleteFormField(
        #     entity_type_other_str="e40_legal_body",
        #     field_id="custom_entity_from_reif",
        # )
        # entity_autocomplete_field_from_reif_rendered = render_to_string(
        #     entity_autocomplete_field_from_reif.template_name,
        #     context={
        #         "entity_autocomplete_field": entity_autocomplete_field_from_reif,
        #         "id_form_field": "id_custom_entity_from_reif",
        #         "autocomplete_url": "/apis/entities/autocomplete/e40_legal_body/",
        #     }
        # )
        # property_autocomplete_field_to_reif_rendered = render_single_autocompletex_form_property(
        #     entity_type_self_str="f10_person",
        #     entity_type_other_str="bookpublicationrelationship",
        #     single_field_id="custom_property_to_reif",
        # )
        # contextual_triple_form_rendered = render_contextual_triple_form(
        #     entity_type_self_str="bookpublicationrelationship",
        #     entity_type_other_str="e40_legal_body",
        #     id_number="0"
        # )
        #
        # reification_form = ReificationForm()
        # context["reification_form"] = render_to_string(
        #     template_name=reification_form.template_name,
        #     context={
        #         "reification_form": reification_form,
        #         "property_autocomplete_field_to_reif_rendered": property_autocomplete_field_to_reif_rendered,
        #         "contextual_triple_form_rendered": contextual_triple_form_rendered,
        #     }
        # )

        # context["reification_table"] = render_to_string(
        #     ReificationTable.template_name_custom, context={"table": ReificationTable()}
        # )
        # context["reification_table_container"] = render_to_string("apis_entities/reification_table_container.html")
        context["reification_form_and_table"] = render_to_string(
            "apis_entities/reification_form_and_table.html",
            context={
                "reification_form": render_reification_form(
                    entity_type_self_str="f10_person",
                    entity_type_reification_str="bookpublicationrelationship",
                    entity_id_self=str(pk),
                ),
                "entity_type_self": "f10_person",
                "entity_type_reification": "bookpublicationrelationship",
                "entity_id_self": str(pk),
                "reification_table": render_reification_table(request),
            },
        )
        return render(request, "apis_entities/entity_create_generic.html", context)

    def post(self, request, *args, **kwargs):
        entity = kwargs['entity']
        pk = kwargs['pk']
        entity_model = AbstractEntity.get_entity_class_of_name(entity)
        instance = get_object_or_404(entity_model, pk=pk)
        form = get_entities_form(entity.title())
        form = form(request.POST, instance=instance)
        form_text = FullTextForm(request.POST, entity=entity.title())
        if form.is_valid() and form_text.is_valid():
            entity_2 = form.save()
            form_text.save(entity_2)
            return redirect(reverse('apis:apis_entities:generic_entities_edit_view', kwargs={
                'pk': pk, 'entity': entity
            }))
        else:
            template = select_template(['apis_entities/{}_create_generic.html'.format(entity),
                                        'apis_entities/entity_create_generic.html'])
            perm = ObjectPermissionChecker(request.user)
            permissions = {'change': perm.has_perm('change_{}'.format(entity), instance),
                           'delete': perm.has_perm('delete_{}'.format(entity), instance),
                           'create': request.user.has_perm('entities.add_{}'.format(entity))}
            context = {
                'form': form,
                'entity_type': entity,
                'form_text': form_text,
                'instance': instance,
                'permissions': permissions}
            if entity.lower() != 'place':
                form_merge_with = GenericEntitiesStanbolForm(entity, ent_merge_pk=pk)
                context['form_merge_with'] = form_merge_with
                return TemplateResponse(request, template, context=context)
            return HttpResponse(template.render(request=request, context=context))



@method_decorator(login_required, name='dispatch')
class GenericEntitiesCreateView(View):
    def get(self, request, *args, **kwargs):
        entity = kwargs['entity']
        form = get_entities_form(entity.title())
        form = form()
        form_text = FullTextForm(entity=entity.title())
        permissions = {'create': request.user.has_perm('entities.add_{}'.format(entity))}
        template = select_template(['apis_entities/{}_create_generic.html'.format(entity),
                                    'apis_entities/entity_create_generic.html'])
        return HttpResponse(template.render(request=request, context={
            'entity_type': entity,
            'permissions': permissions,
            'form': form,
            'form_text': form_text}))

    def post(self, request, *args, **kwargs):
        entity = kwargs['entity']
        form = get_entities_form(entity.title())
        form = form(request.POST)
        form_text = FullTextForm(request.POST, entity=entity.title())
        if form.is_valid() and form_text.is_valid():
            entity_2 = form.save()
            form_text.save(entity_2)
            return redirect(reverse('apis:apis_entities:generic_entities_detail_view', kwargs={
                'pk': entity_2.pk, 'entity': entity
            }))
        else:
            permissions = {'create': request.user.has_perm('apis_entities.add_{}'.format(entity))}
            template = select_template(['apis_entities/{}_create_generic.html'.format(entity),
                                        'apis_entities/entity_create_generic.html'])
            return HttpResponse(template.render(request=request, context={
                'permissions': permissions,
                'form': form,
                'form_text': form_text}))


@method_decorator(login_required, name='dispatch')
class GenericEntitiesCreateStanbolView(View):

    def post(self, request, *args, **kwargs):
        entity = kwargs['entity']
        ent_merge_pk = kwargs.get('ent_merge_pk', False)
        if ent_merge_pk:
            form = GenericEntitiesStanbolForm(entity, request.POST, ent_merge_pk=ent_merge_pk)
        else:
            form = GenericEntitiesStanbolForm(entity, request.POST)
        #form = form(request.POST)
        if form.is_valid():
            entity_2 = form.save()
            if ent_merge_pk:
                entity_2.merge_with(int(ent_merge_pk))
            return redirect(reverse('apis:apis_entities:generic_entities_edit_view', kwargs={
                'pk': entity_2.pk, 'entity': entity
            }))
        else:
            permissions = {'create': request.user.has_perm('apis_entities.add_{}'.format(entity))}
            template = select_template(['apis_entities/{}_create_generic.html'.format(entity),
                                        'apis_entities/entity_create_generic.html'])
            return HttpResponse(template.render(request=request, context={
                'permissions': permissions,
                'form': form}))


@method_decorator(login_required, name='dispatch')
class GenericEntitiesDeleteView(DeleteView):
    # model = ContentType.objects.get(
    #     app_label='apis_entities', model='tempentityclass').model_class()
    model = importlib.import_module("apis_core.apis_entities.models").TempEntityClass
    template_name = getattr(
        settings, 'APIS_DELETE_VIEW_TEMPLATE', 'apis_entities/confirm_delete.html'
    )

    def dispatch(self, request, *args, **kwargs):
        entity = kwargs['entity']
        self.success_url = reverse(
            'apis_core:apis_entities:generic_entities_list', kwargs={'entity': entity}
        )
        return super(GenericEntitiesDeleteView, self).dispatch(request, *args, **kwargs)
