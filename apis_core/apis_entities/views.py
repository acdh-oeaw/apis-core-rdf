# -*- coding: utf-8 -*-
import json

from django.conf import settings
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth.mixins import UserPassesTestMixin
from django.contrib.contenttypes.models import ContentType
from django.http import HttpResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse
from django.urls import reverse_lazy
from django_tables2 import RequestConfig
from django_tables2 import SingleTableView
from django_tables2.export.views import ExportMixin

from apis_core.core.mixins import ListViewObjectFilterMixin

from apis_core.apis_metainfo.models import Uri
from apis_core.utils.stanbolQueries import retrieve_obj
from apis_core.utils.utils import (
    access_for_all,
    access_for_all_function,
    ENTITIES_DEFAULT_COLS,
)
from apis_core.utils.settings import get_entity_settings_by_modelname
from .filters import get_list_filter_of_entity
from .forms import (
    GenericFilterFormHelper,
    PersonResolveUriForm,
)
from .tables import get_entities_table
from apis_core.utils.helpers import get_member_for_entity

###########################################################################
############################################################################
#
#   Helper Functions
#
############################################################################
############################################################################


@user_passes_test(access_for_all_function)
def set_session_variables(request):
    ann_proj_pk = request.GET.get("project", None)
    types = request.GET.getlist("types", None)
    users_show = request.GET.getlist("users_show", None)
    if types:
        request.session["entity_types_highlighter"] = types
    if users_show:
        request.session["users_show_highlighter"] = users_show
    if ann_proj_pk:
        request.session["annotation_project"] = ann_proj_pk
    return request


############################################################################
############################################################################
#
#   GenericViews
#
############################################################################
############################################################################


class GenericListViewNew(
    UserPassesTestMixin, ListViewObjectFilterMixin, ExportMixin, SingleTableView
):
    formhelper_class = GenericFilterFormHelper
    context_filter_name = "filter"
    paginate_by = 25
    template_name = getattr(settings, "APIS_LIST_VIEW_TEMPLATE", "generic_list.html")

    def __init__(self, *args, **kwargs):
        super(GenericListViewNew, self).__init__(*args, **kwargs)
        self.entity = None
        self.filter = None

    def get_model(self):
        """
        Look up the model class for the given entity
        """
        model = ContentType.objects.get(
            app_label__startswith="apis_", model=self.entity
        ).model_class()

        return model

    def test_func(self):
        access = access_for_all(self, viewtype="list")
        if access:
            self.request = set_session_variables(self.request)
        return access

    def get_queryset(self, **kwargs):
        self.entity = self.kwargs.get("entity")

        qs = get_member_for_entity(
            self.get_model(), path="querysets", suffix="ListViewQueryset"
        )
        if qs is None:
            qs = (self.get_model().objects.all()).order_by("name")
        self.filter = get_list_filter_of_entity(self.entity)(
            self.request.GET, queryset=qs
        )
        self.filter.form.helper = self.formhelper_class()

        return self.filter_queryset(self.filter.qs)

    def get_table(self, **kwargs):
        """
        Create entity-specific table object for use on the frontend.

        Holds information on e.g. which fields to use for table columns.
        Incorporates variables provided in Models, Settings where available.

        :return: a dictionary
        """
        model = self.get_model()
        class_name = model.__name__

        session = getattr(self.request, "session", False)

        selected_cols = self.request.GET.getlist(
            "columns"
        )  # populates "Select additional columns" dropdown
        default_cols = []  # get set to "name" in get_entities_table when empty
        entity_settings = get_entity_settings_by_modelname(class_name)
        default_cols = entity_settings.get("table_fields", [])
        default_cols = default_cols + selected_cols

        self.table_class = get_member_for_entity(self.get_model(), suffix="Table")
        if self.table_class is None:
            self.table_class = get_entities_table(class_name, default_cols=default_cols)
        table = super(GenericListViewNew, self).get_table()
        RequestConfig(
            self.request, paginate={"page": 1, "per_page": self.paginate_by}
        ).configure(table)

        return table

    def get_context_data(self, **kwargs):
        """
        Create entity-specific context object for use on the frontend.

        Holds display values and information on functionality based on
        model data as well as variables provided in Settings (where available).

        :return: a dictionary
        """
        context = super(GenericListViewNew, self).get_context_data()
        model = self.get_model()
        class_name = model.__name__

        context[self.context_filter_name] = self.filter
        context["entity"] = self.entity  # model slug
        context["app_name"] = "apis_entities"
        context["docstring"] = f"{model.__doc__}"

        if "browsing" in settings.INSTALLED_APPS:
            from browsing.models import BrowsConf

            context["conf_items"] = list(
                BrowsConf.objects.filter(model_name=class_name).values_list(
                    "field_path", "label"
                )
            )

        # TODO kk
        #  suggestion: rename context['class_name'] to context['entity_name']
        #  throughout (+ same for plural versions) to avoid confusion with
        #  actual model class name
        if model._meta.verbose_name:
            context["class_name"] = f"{model._meta.verbose_name.title()}"
        else:
            context["class_name"] = f"{class_name}"
        if model._meta.verbose_name_plural:
            context["class_name_plural"] = f"{model._meta.verbose_name_plural.title()}"
        # rudimentary way of pluralising the name of a model class
        else:
            if class_name.endswith("s"):
                context["class_name_plural"] = f"{class_name}es"
            elif class_name.endswith("y"):
                context["class_name_plural"] = f"{class_name[:-1]}ies"
            else:
                context["class_name_plural"] = f"{class_name}s"

        try:
            context["get_arche_dump"] = model.get_arche_dump()
        except AttributeError:
            context["get_arche_dump"] = None

        try:
            context["create_view_link"] = model.get_createview_url()
        except AttributeError:
            context["create_view_link"] = None

        toggleable_cols = []
        entity_settings = get_entity_settings_by_modelname(class_name)
        toggleable_cols = entity_settings.get("additional_cols", [])

        # TODO kk spelling of this dict key should get fixed throughout
        #  (togglable_colums -> toggleable_columns)
        context["togglable_colums"] = toggleable_cols + ENTITIES_DEFAULT_COLS

        return context


############################################################################
############################################################################
#
#   OtherViews
#
############################################################################
############################################################################


@user_passes_test(access_for_all_function)
def getGeoJson(request):
    """Used to retrieve GeoJsons for single objects"""
    # if request.is_ajax():
    pk_obj = request.GET.get("object_id")
    instance = get_object_or_404(Place, pk=pk_obj)
    uria = Uri.objects.filter(root_object=instance)
    if uria.count() > 0:
        uric = uria
        add_info = ""
    lst_json = []
    if uric.count() > 0 and not instance.status.startswith("distinct"):
        for x in uric:
            o = retrieve_obj(x.uri)
            if o:
                url_r = reverse_lazy(
                    "apis:apis_entities:resolve_ambigue_place",
                    kwargs={
                        "pk": str(instance.pk),
                        "uri": o["representation"]["id"][7:],
                    },
                )
                select_text = "<a href='{}'>Select this URI</a>".format(url_r)
                try:
                    add_info = "<b>Confidence:</b> {}<br/><b>Feature:</b> <a href='{}'>{}</a>".format(
                        x.confidence, x.uri, x.uri
                    )
                except:
                    add_info = "<b>Confidence:</b>no value provided <br/><b>Feature:</b> <a href='{}'>{}</a>".format(
                        x.uri, x.uri
                    )
                r = {
                    "geometry": {
                        "type": "Point",
                        "coordinates": [
                            float(
                                o["representation"][
                                    "http://www.w3.org/2003/01/geo/wgs84_pos#long"
                                ][0]["value"]
                            ),
                            float(
                                o["representation"][
                                    "http://www.w3.org/2003/01/geo/wgs84_pos#lat"
                                ][0]["value"]
                            ),
                        ],
                    },
                    "type": "Feature",
                    "properties": {
                        "popupContent": "<b>ÖBL name:</b> %s<br/><b>Geonames:</b> %s<br/>%s<br/>%s"
                        % (
                            instance.name,
                            o["representation"][
                                "http://www.geonames.org/ontology#name"
                            ][0]["value"],
                            select_text,
                            add_info,
                        )
                    },
                    "id": x.pk,
                }
                lst_json.append(r)
    elif instance.lat is not None and instance.lng is not None:
        r = {
            "geometry": {"type": "Point", "coordinates": [instance.lng, instance.lat]},
            "type": "Feature",
            "properties": {"popupContent": "<b>Name:</b> %s<br/>" % (instance.name)},
            "id": instance.pk,
        }
        lst_json.append(r)

    return HttpResponse(json.dumps(lst_json), content_type="application/json")


# TODO RDF: Check if this should be removed or adapted
@user_passes_test(access_for_all_function)
def getGeoJsonList(request):
    """Used to retrieve a list of GeoJsons. To generate the list the kind of connection
    and the connected entity is needed"""
    # relation = AbstractRelation.get_relation_class_of_name(request.GET.get("relation"))
    # relation_type = request.GET.get("relation_type")
    objects = relation.objects.filter(related_place__status="distinct").select_related(
        "related_person", "related_place", "relation_type"
    )
    lst_json = []
    for x in objects:
        pers_url = x.related_person.get_absolute_url()
        place_url = x.related_place.get_absolute_url()
        r = {
            "geometry": {
                "type": "Point",
                "coordinates": [x.related_place.lng, x.related_place.lat],
            },
            "type": "Feature",
            "relation_type": x.relation_type.name,
            "properties": {
                "popupContent": "<b>Person:</b> <a href='%s'>%s</a><br/><b>Connection:</b> %s<br/><b>Place:</b> <a href='%s'>%s</a>"
                % (
                    pers_url,
                    x.related_person,
                    x.relation_type,
                    place_url,
                    x.related_place,
                )
            },
            "id": x.pk,
        }
        lst_json.append(r)
    return HttpResponse(json.dumps(lst_json), content_type="application/json")


# TODO RDF: Check if this should be removed or adapted
# @user_passes_test(access_for_all_function)
# def getNetJsonList(request):
#     """Used to retrieve a Json to draw a network"""
#     relation = AbstractRelation.get_relation_class_of_name("PersonPlace")
#     objects = relation.objects.filter(related_place__status="distinct")
#     nodes = dict()
#     edges = []
#
#     for x in objects:
#         if x.related_place.pk not in nodes.keys():
#             place_url = reverse_lazy(
#                 "apis:apis_entities:place_edit", kwargs={"pk": str(x.related_place.pk)}
#             )
#             tt = (
#                 "<div class='arrow'></div>\
#             <div class='sigma-tooltip-header'>%s</div>\
#             <div class='sigma-tooltip-body'>\
#             <table>\
#                 <tr><th>Type</th> <td>%s</td></tr>\
#                 <tr><th>Entity</th> <td><a href='%s'>Link</a></td></tr>\
#             </table>\
#             </div>"
#                 % (x.related_place.name, "place", place_url)
#             )
#             nodes[x.related_place.pk] = {
#                 "type": "place",
#                 "label": x.related_place.name,
#                 "id": str(x.related_place.pk),
#                 "tooltip": tt,
#             }
#         if x.related_person.pk not in nodes.keys():
#             pers_url = reverse_lazy(
#                 "apis:apis_entities:person_edit",
#                 kwargs={"pk": str(x.related_person.pk)},
#             )
#             tt = (
#                 "<div class='arrow'></div>\
#             <div class='sigma-tooltip-header'>%s</div>\
#             <div class='sigma-tooltip-body'>\
#             <table>\
#                 <tr><th>Type</th> <td>%s</td></tr>\
#                 <tr><th>Entity</th> <td><a href='%s'>Link</a></td></tr>\
#             </table>\
#             </div>"
#                 % (str(x.related_person), "person", pers_url)
#             )
#             nodes[x.related_person.pk] = {
#                 "type": "person",
#                 "label": str(x.related_person),
#                 "id": str(x.related_person.pk),
#                 "tooltip": tt,
#             }
#         edges.append(
#             {
#                 "source": x.related_person.pk,
#                 "target": x.related_place.pk,
#                 "kind": x.relation_type.name,
#                 "id": str(x.pk),
#             }
#         )
#     lst_json = {"edges": edges, "nodes": [nodes[x] for x in nodes.keys()]}
#
#     return HttpResponse(json.dumps(lst_json), content_type="application/json")
#
#
# @user_passes_test(access_for_all_function)
# def getNetJsonListInstitution(request):
#     """Used to retrieve a Json to draw a network"""
#     relation = AbstractRelation.get_relation_class_of_name("PersonInstitution")
#     objects = relation.objects.all()
#     nodes = dict()
#     edges = []
#
#     for x in objects:
#         if x.related_institution.pk not in nodes.keys():
#             inst_url = reverse_lazy(
#                 "apis:apis_entities:institution_edit",
#                 kwargs={"pk": str(x.related_institution.pk)},
#             )
#             tt = (
#                 "<div class='arrow'></div>\
#             <div class='sigma-tooltip-header'>%s</div>\
#             <div class='sigma-tooltip-body'>\
#             <table>\
#                 <tr><th>Type</th> <td>%s</td></tr>\
#                 <tr><th>Entity</th> <td><a href='%s'>Link</a></td></tr>\
#             </table>\
#             </div>"
#                 % (x.related_institution.name, "institution", inst_url)
#             )
#             nodes[x.related_institution.pk] = {
#                 "type": "institution",
#                 "label": x.related_institution.name,
#                 "id": str(x.related_institution.pk),
#                 "tooltip": tt,
#             }
#         if x.related_person.pk not in nodes.keys():
#             pers_url = reverse_lazy(
#                 "apis:apis_entities:person_edit",
#                 kwargs={"pk": str(x.related_person.pk)},
#             )
#             tt = (
#                 "<div class='arrow'></div>\
#             <div class='sigma-tooltip-header'>%s</div>\
#             <div class='sigma-tooltip-body'>\
#             <table>\
#                 <tr><th>Type</th> <td>%s</td></tr>\
#                 <tr><th>Entity</th> <td><a href='%s'>Link</a></td></tr>\
#             </table>\
#             </div>"
#                 % (str(x.related_person), "person", pers_url)
#             )
#             nodes[x.related_person.pk] = {
#                 "type": "person",
#                 "label": str(x.related_person),
#                 "id": str(x.related_person.pk),
#                 "tooltip": tt,
#             }
#         edges.append(
#             {
#                 "source": x.related_person.pk,
#                 "target": x.related_institution.pk,
#                 "kind": x.relation_type.name,
#                 "id": str(x.pk),
#             }
#         )
#     lst_json = {"edges": edges, "nodes": [nodes[x] for x in nodes.keys()]}
#
#     return HttpResponse(json.dumps(lst_json), content_type="application/json")
#
#
# @login_required
# def resolve_ambigue_place(request, pk, uri):
#     """Only used to resolve place names."""
#     with reversion.create_revision():
#         uri = "http://" + uri
#         entity = Place.objects.get(pk=pk)
#         pl_n = RDFParser(uri, kind="Place")
#         pl_n.create_objct()
#         pl_n_1 = pl_n.save()
#         pl_n_1 = pl_n.merge(entity)
#         url = pl_n_1.get_absolute_url()
#         if pl_n.created:
#             pl_n_1.status = "distinct (manually resolved)"
#             pl_n_1.save()
#         UriCandidate.objects.filter(entity=entity).delete()
#         reversion.set_user(request.user)
#
#     return HttpResponseRedirect(url)


@login_required
def resolve_ambigue_person(request):
    if request.method == "POST":
        form = PersonResolveUriForm(request.POST)
    if form.is_valid():
        pers = form.save()
        return redirect(
            reverse("apis:apis_entities:person_edit", kwargs={"pk": pers.pk})
        )


############################################################################
############################################################################
#
#  Reversion Views
#
############################################################################
############################################################################
# TODO: add again as soon as the module has been bumped to new django version
# class ReversionCompareView(HistoryCompareDetailView):
#    template_name = 'apis_entities/compare_base.html'

#    def dispatch(self, request, app, kind, pk, *args, **kwargs):
#        self.model = ContentType.objects.get(app_label=app, model=kind).model_class()
#        return super(ReversionCompareView, self).dispatch(request, *args, **kwargs)
