# -*- coding: utf-8 -*-
import json

from apis_core.apis_metainfo.models import Text, Uri, UriCandidate
from apis_core.utils.stanbolQueries import retrieve_obj
from apis_core.utils.utils import (
    ENTITIES_DEFAULT_COLS,
    access_for_all,
    access_for_all_function,
)
from django.conf import settings
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth.mixins import UserPassesTestMixin
from django.contrib.contenttypes.models import ContentType
from django.core.exceptions import ImproperlyConfigured
from django.http import HttpResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse, reverse_lazy
from django_tables2 import SingleTableView
from django_tables2.export.views import ExportMixin

from .filters import get_list_filter_of_entity
from .forms import (
    GenericEntitiesStanbolForm,
    GenericFilterFormHelper,
    NetworkVizFilterForm,
    PersonResolveUriForm,
)
from .tables import EntitiesTableFactory, get_entities_table

if "apis_highlighter" in settings.INSTALLED_APPS:
    from apis_highlighter.forms import SelectAnnotationProject
    from apis_highlighter.highlighter import highlight_text_new

if "charts" in settings.INSTALLED_APPS:
    from charts.models import ChartConfig
    from charts.views import create_payload

if "browsing" in settings.INSTALLED_APPS:
    import datetime
    import time

    import pandas as pd
    from browsing.models import BrowsConf

    browsing_is_installed = True
else:
    browsing_is_installed = False

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
    edit_views = request.GET.get("edit_views", False)
    if types:
        request.session["entity_types_highlighter"] = types
    if users_show:
        request.session["users_show_highlighter"] = users_show
    if ann_proj_pk:
        request.session["annotation_project"] = ann_proj_pk
    if edit_views:
        if edit_views != "false":
            request.session["edit_views"] = True
    return request


@user_passes_test(access_for_all_function)
def get_highlighted_texts(request, instance):
    if "apis_highlighter" in settings.INSTALLED_APPS:
        set_ann_proj = request.session.get("annotation_project", 1)
        entity_types_highlighter = request.session.get(
            "entity_types_highlighter", None
        )
        users_show = request.session.get("users_show_highlighter", None)
        object_texts = [
            {
                "text": highlight_text_new(
                    x,
                    set_ann_proj=set_ann_proj,
                    types=entity_types_highlighter,
                    users_show=users_show,
                )[0].strip(),
                "id": x.pk,
                "kind": x.kind,
            }
            for x in Text.objects.filter(tempentityclass=instance)
        ]
        ann_proj_form = SelectAnnotationProject(
            set_ann_proj=set_ann_proj,
            entity_types_highlighter=entity_types_highlighter,
            users_show_highlighter=users_show,
        )
        return object_texts, ann_proj_form
    else:
        object_texts = [
            {"text": x.text, "id": x.pk, "kind": x.kind}
            for x in Text.objects.filter(tempentityclass=instance)
        ]
        return object_texts, False


############################################################################
############################################################################
#
#   GenericViews
#
############################################################################
############################################################################


class GenericTableViewMixin(ExportMixin, SingleTableView):
    """
    Yeah, not really a pure Mixin if it has a view in it... So 'needs' refactor.
    But there was no point in making it completely standalone and reusable yet, before
    refactor of all the table classes and app-structure of apis-rdf is decided. So:
    NOTE: __gp__: consider renaming it, if it will not become a standalone mixin. ATM it is, as the name says, a hybrid between a Mixin and a View.
    I still think that it makes very much sense to extract the table specific logic into it's own class to improve readability.
    """

    # 'inherited' class-attribute. will be passed to instance as self.table_pagination and used by methods of SingleTableView! Don't rename!
    table_pagination = {"page": 1, "per_page": 25}
    table_factory_class = EntitiesTableFactory

    def get(self, request, *args, **kwargs):
        self.model_name = kwargs.get("entity", None)

        # 'inherited' attr! Has logic attached to it, i.e. is potentially used by internal methods of parent-classes!
        self.model_class = ContentType.objects.get(
            app_label__startswith="apis_", model=self.model_name
        ).model_class()

        # TODO: __gp__: this naming prevents real generic use of this "mixin". Rename with refactor.
        self.entity_settings = self.get_entity_settings()

        return super().get(request, *args, **kwargs)

    def get_table_class(self):
        """
        Inherited method from SingleTableMixin via SingleTableView.
        """
        if self.table_class:
            return self.table_class
        elif hasattr(self, "table_factory_class"):
            return self.table_factory_class.get_table_class(self.model_class)

        raise ImproperlyConfigured(
            f"You must either specify {type(self).__name__}.table_class or"
            " provide a factory-class as"
            f" {type(self).__name__}.table_factory_class"
        )

    def get_entity_settings(self):
        """
        Custom method, not inherited.
        TODO: __gp__: this naming prevents real generic use of this "mixin". Should be refactored for reusability and moved outside of apis_entities.
        """

        if hasattr(self.model_class, "entity_settings"):
            return self.model_class.entity_settings
        else:
            return {}

    def get_columns_selected_by_user(self):
        """
        Custom method, not inherited. Implemented for extensibility and readability.
        Context-Info: User can select additional columns from a dropdown in frontend.
        """

        selected_cols = self.request.GET.getlist("columns")
        return selected_cols

    def get_default_columns_for_model(self):
        """
        Custom method, not inherited.
        Reads the default column(s) for the model from your projects-file.
        If not defined or left empty, defaults to ['name'].
        """

        if hasattr(settings, "APIS_ENTITIES"):
            class_settings = settings.APIS_ENTITIES.get(self.model_name, {})
            return class_settings.get("table_fields", ["name"])
        else:
            return [
                "name",
            ]

    def get_table_kwargs(self):
        """
        Overwrites method from SingleTableMixin via SingleTableView.
        Sourcecode with docstring: https://django-tables2.readthedocs.io/en/latest/_modules/django_tables2/views.html#SingleTableMixin

        >>>>>>>> IMPORTANT: Customization of a table instance in a concrete use-context should happen in this method! <<<<<<<

        Returns a dict of kwargs used to instanciate the table from the given table_class (implicitly, via methods of the super-classes!).
        If you need entity specific configurations, apply them here - see dummy if branch!.
        """
        kwargs = {}

        columns = (
            self.get_default_columns_for_model()
            + self.get_columns_selected_by_user()
        )

        if self.request.user.is_authenticated:
            # apply configurations that need authentication; visible_columns is a custom param passed to the Tables __init__!
            kwargs["visible_columns"] = ("_detail", "_edit", *columns)
            kwargs["sequence"] = ("_detail", "_edit", "...")
        else:
            kwargs["visible_columns"] = ("_detail", *columns)
            kwargs["sequence"] = ("_detail", "...")

        # __gp__: Apply entity specific configurations here:
        if self.model_name == "ExampleDummyName":
            # __gp__: overwrite all or specific kwargs here.
            # for example: you can add more Columns, even ones that are not defined on the table-class here.
            # or you can change styling by changing the attrs - keyword.
            # etc.
            pass

        return kwargs

    def get_context_data(self):
        """
        Contributes table-specific keys to the inheriting get_context_data - method.
        """

        enable_merge = (
            self.entity_settings.get("merge", False)
            if self.request.user.is_authenticated
            else False
        )

        def get_toggleable_columns():
            cols = ENTITIES_DEFAULT_COLS + self.entity_settings.get(
                "additional_cols", []
            )

            if enable_merge:
                cols.append("merge")

            return cols

        context = super().get_context_data()
        context.update(
            {
                "togglable_columns": get_toggleable_columns(),
                "enable_merge": enable_merge,
            }
        )

        return context


class GenericListViewNew(UserPassesTestMixin, GenericTableViewMixin):
    formhelper_class = GenericFilterFormHelper
    template_name = getattr(
        settings, "APIS_LIST_VIEW_TEMPLATE", "browsing/generic_list.html"
    )
    login_url = "/accounts/login/"

    def test_func(self):
        """
        Test function expected by the UserPassesTestMixin.
        Tests if user passes condition.
        """
        access = access_for_all(self, viewtype="list")
        if access:
            self.request = set_session_variables(self.request)
        return access

    def get_queryset(self, **kwargs):
        qs = (self.model_class.objects.all()).order_by("name")
        self.filter = get_list_filter_of_entity(self.model_name)(
            self.request.GET, queryset=qs
        )
        self.filter.form.helper = self.formhelper_class()

        return self.filter.qs

    def get_context_data(self, **kwargs):
        """
        Overwrites inherited method. Prepares the context dict which makes additional data available in templates.

        Important: in the context of tables, the actual calls to the inherited method get_table and get_table_data from SingleTableMixin and our own Mixin
        (see https://django-tables2.readthedocs.io/en/latest/_modules/django_tables2/views.html#SingleTableMixin) are hidden behind the
        call to super().get_context_data(). This call contributes f.e. the 'table' key to the context dict, which is then rendered in the template. Just a general
        note that you can't really reason about what the code does.

        :return: dict
        """
        model_class = self.model_class
        model_name = self.model_name

        def get_model_name_plural():
            """
            Refactored into an inner function for readability.
            TODO: __gpirgie__: pls make this an external util function that can be re-used in different contexts.\
                  Or implement this logic on our Base-Models (another case for a mixin, maybe).
            """
            if model_class._meta.verbose_name_plural:
                return model_class._meta.verbose_name_plural.title()
            # rudimentary way of pluralising the name of a model class
            else:
                if model_name.endswith("s"):
                    return f"{model_name}es"
                elif model_name.endswith("y"):
                    return f"{model_name[:-1]}ies"
                else:
                    return f"{model_name}s"

        context = super().get_context_data()
        context.update(
            {
                "filter": self.filter,
                "app_name": "apis_entities",  # TODO: __gp__: this should also not be hardcoded. See if branch in 'charts' below: should app_label not be the same value/variable?
                "docstring": str(model_class.__doc__),
                "entitiy_create_stanbol": GenericEntitiesStanbolForm(
                    model_name
                ),
                "class_name": model_name
                if not model_class._meta.verbose_name
                else model_class._meta.verbose_name.title(),  # TODO: __gp__: as already noted by kk, class_name should be renamed also in templates.
                "class_name_plural": get_model_name_plural(),
                "get_arche_dump": None
                if not hasattr(model_class, "get_arche_dump")
                else model_class.get_arche_dump(),
                "create_view_link": None
                if not hasattr(model_class, "get_createview_url")
                else model_class.get_createview_url(),
            }
        )

        # TODO: __gp__: once the download functionality from the browsing/charts module is re-implemented, consider moving this logic (and the render logic) to a separate mixin.
        if browsing_is_installed:
            context["conf_items"] = list(
                BrowsConf.objects.filter(model_name=model_name).values_list(
                    "field_path", "label"
                )
            )

        if "charts" in settings.INSTALLED_APPS:
            app_label = (
                model_class._meta.app_label
            )  # see comment on context.update({... "app_name": "apis_entities" above.
            filtered_objs = ChartConfig.objects.filter(
                model_name=model_class.__name__.lower(), app_name=app_label
            )
            context["vis_list"] = filtered_objs
            context["property_name"] = self.request.GET.get("property")
            context["charttype"] = self.request.GET.get("charttype")
            if context["charttype"] and context["property_name"]:
                qs = self.get_queryset()
                chartdata = create_payload(
                    context["entity"],
                    context["property_name"],
                    context["charttype"],
                    qs,
                    app_label=app_label,
                )
                context = dict(context, **chartdata)

        return context

    def render_to_response(self, context, **kwargs):
        download = self.request.GET.get("sep", None)

        # TODO: __gp__: once the download functionality from the browsing/charts module is re-implemented, consider moving this logic to a separate mixin/class and improve readability.
        def http_response_with_attachment():
            """
            Moved into inner function for readability.
            """
            sep = self.request.GET.get("sep", ",")
            timestamp = datetime.datetime.fromtimestamp(time.time()).strftime(
                "%Y-%m-%d-%H-%M-%S"
            )
            filename = "export_{}".format(timestamp)
            response = HttpResponse(content_type="text/csv")
            if context["conf_items"]:
                conf_items = context["conf_items"]
                try:
                    df = pd.DataFrame(
                        list(
                            self.get_queryset().values_list(
                                *[x[0] for x in conf_items]
                            )
                        ),
                        columns=[x[1] for x in conf_items],
                    )
                except AssertionError:
                    response[
                        "Content-Disposition"
                    ] = 'attachment; filename="{}.csv"'.format(filename)
                    return response
            else:
                response[
                    "Content-Disposition"
                ] = 'attachment; filename="{}.csv"'.format(filename)
                return response

            sep_mapp = {"comma": ",", "semicolon": ";", "tab": "\t"}

            df.to_csv(response, sep=sep_mapp.get(sep, ","), index=False)

            response[
                "Content-Disposition"
            ] = 'attachment; filename="{}.csv"'.format(filename)
            return response

        if download and browsing_is_installed:
            return http_response_with_attachment()
        else:
            return super(GenericListViewNew, self).render_to_response(context)


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
    urib = UriCandidate.objects.filter(entity=instance)
    if urib.count() > 0:
        uric = urib
    elif uria.count() > 0:
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
                    add_info = (
                        "<b>Confidence:</b> {}<br/><b>Feature:</b> <a"
                        " href='{}'>{}</a>".format(x.confidence, x.uri, x.uri)
                    )
                except:
                    add_info = (
                        "<b>Confidence:</b>no value provided"
                        " <br/><b>Feature:</b> <a href='{}'>{}</a>".format(
                            x.uri, x.uri
                        )
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
                        "popupContent": (
                            "<b>ÖBL name:</b> %s<br/><b>Geonames:</b>"
                            " %s<br/>%s<br/>%s"
                        )
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
            "geometry": {
                "type": "Point",
                "coordinates": [instance.lng, instance.lat],
            },
            "type": "Feature",
            "properties": {
                "popupContent": "<b>Name:</b> %s<br/>" % (instance.name)
            },
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
    objects = relation.objects.filter(
        related_place__status="distinct"
    ).select_related("related_person", "related_place", "relation_type")
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
                "popupContent": (
                    "<b>Person:</b> <a href='%s'>%s</a><br/><b>Connection:</b>"
                    " %s<br/><b>Place:</b> <a href='%s'>%s</a>"
                )
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
#   VisualizationViews
#
############################################################################
############################################################################


@user_passes_test(access_for_all_function)
def birth_death_map(request):
    return render(request, "apis:apis_entities/map_list.html")


@user_passes_test(access_for_all_function)
def pers_place_netw(request):
    return render(request, "apis:apis_entities/network.html")


@user_passes_test(access_for_all_function)
def pers_inst_netw(request):
    return render(request, "apis:apis_entities/network_institution.html")


@user_passes_test(access_for_all_function)
def generic_network_viz(request):
    if request.method == "GET":
        form = NetworkVizFilterForm()
        return render(
            request,
            "apis:apis_entities/generic_network_visualization.html",
            {"form": form},
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
