from django.conf import settings
from django.http import HttpResponse
from django.template.loader import select_template
from django.views import View
from django.forms.models import model_to_dict

from apis_core.apis_metainfo.models import Uri
from apis_core.utils.settings import get_entity_settings_by_modelname
from apis_core.apis_entities.mixins import EntityInstanceMixin
from apis_core.core.mixins import ViewPassesTestMixin
from apis_core.utils import helpers


class GenericEntitiesDetailView(ViewPassesTestMixin, EntityInstanceMixin, View):
    def get(self, request, *args, **kwargs):

        entity = self.entity.lower()

        side_bar = helpers.triple_sidebar(self.pk, self.entity, request)

        # TODO RDF : Check / Adapt the following code to rdf architecture
        object_lod = Uri.objects.filter(root_object=self.instance)
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

        relevant_fields = []
        entity_settings = get_entity_settings_by_modelname(self.entity)
        exclude_fields = entity_settings.get("detail_view_exclude", [])
        for field, value in model_to_dict(self.instance).items():
            if field not in exclude_fields:
                relevant_fields.append((self.instance._meta.get_field(field), value))

        return HttpResponse(
            template.render(
                request=request,
                context={
                    "entity_type": entity,
                    "object": self.instance,
                    "relevant_fields": relevant_fields,
                    "right_card": side_bar,
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
