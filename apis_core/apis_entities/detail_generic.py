from django.conf import settings
from django.contrib.auth.mixins import UserPassesTestMixin
from django.contrib.contenttypes.models import ContentType
from django.db.models import Q
from django.http import HttpResponse
from django.shortcuts import get_object_or_404
from django.template.loader import select_template
from django.views import View
from django_tables2 import RequestConfig
from django.forms.models import model_to_dict

from apis_core.apis_labels.models import Label
from apis_core.apis_metainfo.models import Uri
from apis_core.apis_relations.tables import (
    get_generic_triple_table,
    LabelTableBase,
)
from apis_core.utils.utils import access_for_all
from apis_core.apis_relations.models import TempTriple
from apis_core.utils import caching
from apis_core.utils.settings import get_entity_settings_by_modelname
from apis_core.apis_entities.mixins import EntityInstanceMixin
from apis_core.core.mixins import ViewPassesTestMixin


class GenericEntitiesDetailView(ViewPassesTestMixin, EntityInstanceMixin, View):
    def get(self, request, *args, **kwargs):

        entity = self.entity.lower()
        side_bar = []

        triples_related_all = (
            TempTriple.objects_inheritance.filter(
                Q(subj__pk=self.pk) | Q(obj__pk=self.pk)
            )
            .all()
            .select_subclasses()
        )

        for entity_class in caching.get_all_entity_classes():

            entity_content_type = ContentType.objects.get_for_model(entity_class)

            other_entity_class_name = entity_class.__name__.lower()

            triples_related_by_entity = triples_related_all.filter(
                (Q(subj__self_contenttype=entity_content_type) & Q(obj__pk=self.pk))
                | (Q(obj__self_contenttype=entity_content_type) & Q(subj__pk=self.pk))
            )

            table = get_generic_triple_table(
                other_entity_class_name=other_entity_class_name,
                entity_pk_self=self.pk,
                detail=True,
            )

            prefix = f"{other_entity_class_name}"
            title_card = prefix
            match = [prefix]
            tb_object = table(data=triples_related_by_entity, prefix=prefix)
            tb_object_open = request.GET.get(prefix + "page", None)
            entity_settings = get_entity_settings_by_modelname(entity_class.__name__)
            per_page = entity_settings.get("relations_per_page", 10)
            RequestConfig(request, paginate={"per_page": per_page}).configure(tb_object)
            side_bar.append(
                (
                    title_card,
                    tb_object,
                    "".join([x.title() for x in match]),
                    tb_object_open,
                )
            )

        # TODO RDF : Check / Adapt the following code to rdf architecture
        object_lod = Uri.objects.filter(root_object=self.instance)
        object_labels = Label.objects.filter(temp_entity__id=self.instance.id)
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
            tei = set(tei)
        ceteicean_css = getattr(settings, "APIS_CETEICEAN_CSS", None)
        ceteicean_js = getattr(settings, "APIS_CETEICEAN_JS", None)
        openseadragon_js = getattr(settings, "APIS_OSD_JS", None)
        openseadragon_img = getattr(settings, "APIS_OSD_IMG_PREFIX", None)
        iiif_field = getattr(settings, "APIS_IIIF_WORK_KIND", None)
        if iiif_field:
            try:
                if "{}".format(self.instance.kind) == "{}".format(iiif_field):
                    iiif = True
                else:
                    iiif = False
            except AttributeError:
                iiif = False
        else:
            iiif = False
        iiif_server = getattr(settings, "APIS_IIIF_SERVER", None)
        iiif_info_json = self.instance.name
        try:
            no_merge_labels = [
                x for x in object_labels if not x.label_type.name.startswith("Legacy")
            ]
        except AttributeError:
            no_merge_labels = []

        relevant_fields = []
        for field in model_to_dict(self.instance).keys():
            relevant_fields.append(
                (self.instance._meta.get_field(field), getattr(self.instance, field))
            )

        return HttpResponse(
            template.render(
                request=request,
                context={
                    "entity_type": entity,
                    "object": self.instance,
                    "relevant_fields": relevant_fields,
                    "right_card": side_bar,
                    "no_merge_labels": no_merge_labels,
                    "object_lables": object_labels,
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
