from django.conf import settings
from django.contrib.auth.mixins import UserPassesTestMixin
from django.db.models import Q
from django.http import HttpResponse
from django.shortcuts import get_object_or_404
from django.template.loader import select_template
from django.views import View
from django_tables2 import RequestConfig
from apis_core.apis_labels.models import Label
from apis_core.apis_metainfo.models import Uri
from apis_core.apis_relations.tables import get_generic_relations_table, get_generic_triple_table, \
    LabelTableBase, render_triple_table, render_reification_table  # , EntityDetailViewLabelTable
from apis_core.helper_functions.utils import access_for_all
from apis_core.apis_entities.models import AbstractEntity
from apis_core.apis_entities.views import get_highlighted_texts
from apis_core.apis_relations.models import Triple, Property, AbstractReification
from apis_core.apis_relations.forms import render_triple_form_and_table, render_reification_form_and_table
from apis_core.helper_functions import caching


class GenericEntitiesDetailView(UserPassesTestMixin, View):
    login_url = '/accounts/login/'
    
    def test_func(self):
        access = access_for_all(self, viewtype="detail")
        return access
    
    def get(self, request, *args, **kwargs):
        entity_self_type_str = kwargs['entity'].lower()
        entity_self_id = kwargs['pk']
        entity_self_class = caching.get_ontology_class_of_name(entity_self_type_str)
        entity_self_content_type = caching.get_contenttype_of_class(entity_self_class)
        entity_self_instance = get_object_or_404(entity_self_class, pk=entity_self_id)
        triple_pane = []
        # Iterate over all entity and reification classes for the relation view on the right pane
        for model_other_class in caching.get_all_entity_classes() + caching.get_all_reification_classes():
            model_other_contenttype = caching.get_contenttype_of_class(model_other_class)
            model_other_class_str = model_other_class.__name__.lower()
            allowed_property_list = Property.objects.filter(
                Q(subj_class=entity_self_content_type, obj_class=model_other_contenttype)
                | Q(subj_class=model_other_contenttype, obj_class=entity_self_content_type)
            )
            if len(allowed_property_list) > 0:
                # check if there are any relations to that respective class
                related_triple_list = Triple.objects.filter(
                    (
                        Q(subj=entity_self_instance)
                        & Q(obj__self_content_type=model_other_contenttype)
                    )
                    | (
                        Q(obj=entity_self_instance)
                        & Q(subj__self_content_type=model_other_contenttype)
                    )
                ).distinct()
                # only load when there are relations
                if len(related_triple_list) > 0:
                    # if it's an entity class, load a simple triple table
                    if issubclass(model_other_class, AbstractEntity):
                        relation_form = render_triple_table(
                            model_self_class_str=entity_self_type_str,
                            model_other_class_str=model_other_class_str,
                            model_self_id_str=str(entity_self_id),
                            should_be_editable=False,
                            request=request,
                        )
                    # if it's an reification class, load the reification table
                    elif issubclass(model_other_class, AbstractReification):
                        relation_form = render_reification_table(
                            model_self_class_str=entity_self_type_str,
                            reification_type_str=model_other_class_str,
                            model_self_id_str=str(entity_self_id),
                            should_be_editable=False,
                            request=request,
                        )
                    # to be sure the surrounding code has not been wrongly modified
                    else:
                        raise Exception("An invalid related entity class was passed")
                    triple_pane.append({
                        "title": f"{model_other_class_str}",
                        "triple_form_and_table": relation_form,
                    })
        # TODO RDF : Check / Adapt the following code to rdf architecture
        object_lod = Uri.objects.filter(root_object=entity_self_instance)
        object_texts, ann_proj_form = get_highlighted_texts(request, entity_self_instance)
        object_labels = Label.objects.filter(temp_entity=entity_self_instance)
        tb_label = LabelTableBase(data=object_labels, prefix=entity_self_type_str.title()[:2]+'L-')
        tb_label_open = request.GET.get('PL-page', None)
        # triple_pane.append(('Label', tb_label, 'PersonLabel', tb_label_open))
        RequestConfig(request, paginate={"per_page": 10}).configure(tb_label)
        template = select_template([
            # 'apis_entities/detail_views/{}_detail_generic.html'.format(entity),
            'apis_entities/detail_views/entity_detail_generic.html'
        ])
        tei = getattr(settings, "APIS_TEI_TEXTS", [])
        if tei:
            tei = set(tei) & set([x.kind.name for x in entity_self_instance.text.all()])
        ceteicean_css = getattr(settings, "APIS_CETEICEAN_CSS", None)
        ceteicean_js = getattr(settings, "APIS_CETEICEAN_JS", None)
        openseadragon_js = getattr(settings, "APIS_OSD_JS", None)
        openseadragon_img = getattr(settings, "APIS_OSD_IMG_PREFIX", None)
        iiif_field = getattr(settings, "APIS_IIIF_WORK_KIND", None)
        if iiif_field:
            try:
                if "{}".format(entity_self_instance.kind) == "{}".format(iiif_field):
                    iiif = True
                else:
                    iiif = False
            except AttributeError:
                iiif = False
        else:
            iiif = False
        iiif_server = getattr(settings, "APIS_IIIF_SERVER", None)
        iiif_info_json = entity_self_instance.name
        try:
            no_merge_labels = [
                x for x in object_labels if not x.label_type.name.startswith('Legacy')
            ]
        except AttributeError:
            no_merge_labels = []
        
        # TODO : Hackish work-around, do this more properly later
        def get_relevant_fields(instance):
            
            list_key_val_pairs = []
            attr_to_exclude = [
                "id",
                "name",
                "self_content_type_id",
                "start_start_date",
                "start_end_date",
                "end_start_date",
                "end_end_date",
                "start_date_written",
                "end_date_written",
                "status",
                "source_id",
                "references",
                "notes",
                "published",
                "references",
                "collection",
                "review",
                "text",
            ]
            for f in instance._meta.get_fields():
                if hasattr(f, "attname"):
                    if (
                        not f.attname.endswith("_ptr_id")
                        and f.attname not in attr_to_exclude
                    ):
                        list_key_val_pairs.append((f.attname, getattr(instance, f.attname)))
            
            return list_key_val_pairs
        
        relvant_fields = get_relevant_fields(entity_self_instance)
        
        return HttpResponse(template.render(
            request=request, context={
                'entity_type': entity_self_type_str,
                'object': entity_self_instance,
                'relvant_fields': relvant_fields,
                'triple_pane': triple_pane,
                'no_merge_labels': no_merge_labels,
                'object_lables': object_labels,
                'object_texts': object_texts,
                'object_lod': object_lod,
                'tei': tei,
                'ceteicean_css': ceteicean_css,
                'ceteicean_js': ceteicean_js,
                'iiif': iiif,
                'openseadragon_js': openseadragon_js,
                'openseadragon_img': openseadragon_img,
                'iiif_field': iiif_field,
                'iiif_info_json': iiif_info_json,
                'iiif_server': iiif_server,
            }
        ))
