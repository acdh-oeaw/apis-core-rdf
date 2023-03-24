from django.conf import settings
from django.contrib.auth.mixins import UserPassesTestMixin
from django.contrib.contenttypes.models import ContentType
from django.db.models import Q
from django.http import HttpResponse
from django.shortcuts import get_object_or_404
from django.template.loader import select_template
from django.views import View
from django_tables2 import RequestConfig
from apis_core.apis_labels.models import Label
from apis_core.apis_metainfo.models import Uri
from apis_core.apis_relations.tables import (
    get_generic_relations_table,
    get_generic_triple_table,
    LabelTableBase,
)
from apis_core.helper_functions.utils import access_for_all
from apis_core.apis_entities.models import AbstractEntity
from .views import get_highlighted_texts
from apis_core.apis_relations.models import TempTriple
from ..helper_functions import caching


class GenericEntitiesDetailView(UserPassesTestMixin, View):

    login_url = "/accounts/login/"

    def test_func(self):
        access = access_for_all(self, viewtype="detail")
        return access

    def get(self, request, *args, **kwargs):

        entity = kwargs["entity"].lower()
        pk = kwargs["pk"]
        entity_model = caching.get_entity_class_of_name(entity)
        instance = get_object_or_404(entity_model, pk=pk)
        side_bar = []

        triples_related_all = (
            TempTriple.objects_inheritance.filter(Q(subj__pk=pk) | Q(obj__pk=pk))
            .all()
            .select_subclasses()
        )

        for entity_class in caching.get_all_entity_classes():

            entity_content_type = ContentType.objects.get_for_model(entity_class)

            other_entity_class_name = entity_class.__name__.lower()

            triples_related_by_entity = triples_related_all.filter(
                (
                    Q(subj__self_contenttype=entity_content_type)
                    & Q(obj__pk=pk)
                )
                | (Q(obj__self_contenttype=entity_content_type) & Q(subj__pk=pk))
            )

            table = get_generic_triple_table(
                other_entity_class_name=other_entity_class_name,
                entity_pk_self=pk,
                detail=True,
            )

            prefix = f"{other_entity_class_name}"
            title_card = prefix
            match = [prefix]
            tb_object = table(data=triples_related_by_entity, prefix=prefix)
            tb_object_open = request.GET.get(prefix + "page", None)
            RequestConfig(request, paginate={"per_page": 10}).configure(tb_object)
            side_bar.append(
                (
                    title_card,
                    tb_object,
                    "".join([x.title() for x in match]),
                    tb_object_open,
                )
            )

        # TODO RDF : Check / Adapt the following code to rdf architecture
        object_lod = Uri.objects.filter(root_object=instance)
        object_texts, ann_proj_form = get_highlighted_texts(request, instance)
        object_labels = Label.objects.filter(temp_entity=instance)
        tb_label = LabelTableBase(data=object_labels, prefix=entity.title()[:2] + "L-")
        tb_label_open = request.GET.get("PL-page", None)
        side_bar.append(("Label", tb_label, "PersonLabel", tb_label_open))
        RequestConfig(request, paginate={"per_page": 10}).configure(tb_label)
        template = select_template(
            [
                "apis_entities/detail_views/{}_detail_generic.html".format(entity),
                "apis_entities/detail_views/detail_generic.html",
            ]
        )
        tei = getattr(settings, "APIS_TEI_TEXTS", [])
        if tei:
            tei = set(tei) & set([x.kind.name for x in instance.text.all()])
        ceteicean_css = getattr(settings, "APIS_CETEICEAN_CSS", None)
        ceteicean_js = getattr(settings, "APIS_CETEICEAN_JS", None)
        openseadragon_js = getattr(settings, "APIS_OSD_JS", None)
        openseadragon_img = getattr(settings, "APIS_OSD_IMG_PREFIX", None)
        iiif_field = getattr(settings, "APIS_IIIF_WORK_KIND", None)
        if iiif_field:
            try:
                if "{}".format(instance.kind) == "{}".format(iiif_field):
                    iiif = True
                else:
                    iiif = False
            except AttributeError:
                iiif = False
        else:
            iiif = False
        iiif_server = getattr(settings, "APIS_IIIF_SERVER", None)
        iiif_info_json = instance.name
        try:
            no_merge_labels = [
                x for x in object_labels if not x.label_type.name.startswith("Legacy")
            ]
        except AttributeError:
            no_merge_labels = []

        # TODO : Hackish work-around, do this more properly later
        def get_relevant_fields(instance):

            list_key_val_pairs = []
            attr_to_exclude = [
                "id",
                "name",
                "self_contenttype_id",
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
                        list_key_val_pairs.append(
                            (f.attname, getattr(instance, f.attname))
                        )

            return list_key_val_pairs

        relvant_fields = get_relevant_fields(instance)

        return HttpResponse(
            template.render(
                request=request,
                context={
                    "entity_type": entity,
                    "object": instance,
                    "relvant_fields": relvant_fields,
                    "right_card": side_bar,
                    "no_merge_labels": no_merge_labels,
                    "object_lables": object_labels,
                    "object_texts": object_texts,
                    "object_lod": object_lod,
                    "tei": tei,
                    "ceteicean_css": ceteicean_css,
                    "ceteicean_js": ceteicean_js,
                    "iiif": iiif,
                    "openseadragon_js": openseadragon_js,
                    "openseadragon_img": openseadragon_img,
                    "iiif_field": iiif_field,
                    "iiif_info_json": iiif_info_json,
                    "iiif_server": iiif_server,
                },
            )
        )
