import django_tables2 as tables
from django.conf import settings
from django.db.models import Case, When, F, Q
from django.template.loader import render_to_string
from django.utils.html import format_html
from django_tables2.utils import A
from apis_core.apis_entities.models import AbstractEntity
from apis_core.apis_labels.models import Label
from apis_core.apis_metainfo.models import Uri
from apis_core.apis_metainfo.tables import (
    generic_order_start_date_written,
    generic_order_end_date_written,
    generic_render_start_date_written,
    generic_render_end_date_written,
)
from apis_core.apis_relations.models import Triple, Property
from apis_core.helper_functions import caching

empty_text_default = "There are currently no relations"


def render_triple_table(
    model_self_class_str,
    model_other_class_str,
    model_self_id_str,
    should_be_editable,
    request,
):
    """
    renders the table of properties and entities of related triples. To be used for a quick
    overview in an entity detail or edit view. Also, if needed with ajax calls prepared and
    integrated into the rows for edit and delete purpose.

    :param model_self_class_str: str representation of the main entity class, always referred as
    self, in django's lowercase format
    :param model_other_class_str: str representation of the other entity class, always referred as
    self, in django's lowercase format
    :param model_self_id_str: the id of the main entity instance, needed for creating triples
    :param should_be_editable: toggle if this should be rendered with edit buttons or not (for
    entity detail and edit view separately)
    :param request: the request object, needed for the table for whatever reason. Could not leave
    it out.
    :return: a html rendered string to be integrated into the calling view
    """

    class TripleTable(tables.Table):
        # Since the main entity can be either subject or object of a triple, we need 'other' fields
        other_prop = tables.Column(empty_values=())
        other_entity = tables.Column(empty_values=())
        if should_be_editable:
            edit = tables.Column(empty_values=())
            delete = tables.Column(empty_values=())

        class Meta:
            model = Triple
            fields = ["other_prop", "other_entity"]
            if should_be_editable:
                fields += ["edit", "delete"]
                if "apis_bibsonomy" in settings.INSTALLED_APPS:
                    fields = ["ref"] + fields
            # If I would use `template_name` here, django-tables crashes. Perhaps it only expects some
            # of its own pre-integrated templates? But since I want to use a custom one and also attach it
            # to this class I renamed it to `template_name_custom`. I did not find a better solution quickly.
            template_name_custom = "apis_relations/triple_table.html"

        def __init__(self, *args, **kwargs):
            model_self_class = caching.get_ontology_class_of_name(model_self_class_str)
            model_self_instance = model_self_class.objects.get(pk=model_self_id_str)
            model_other_class = caching.get_ontology_class_of_name(
                model_other_class_str
            )
            model_other_contenttype = caching.get_contenttype_of_class(
                model_other_class
            )
            # get the data that is only related to current main entity
            data = Triple.objects.filter(
                (
                    Q(subj=model_self_instance)
                    & Q(obj__self_contenttype=model_other_contenttype)
                )
                | (
                    Q(obj=model_self_instance)
                    & Q(subj__self_contenttype=model_other_contenttype)
                )
            ).distinct()
            self.base_columns["other_prop"].verbose_name = "Other property"
            self.base_columns[
                "other_entity"
            ].verbose_name = f"Related {model_other_class.__name__.title()}"
            if "apis_bibsonomy" in settings.INSTALLED_APPS:
                self.base_columns["ref"] = tables.TemplateColumn(
                    template_name="apis_relations/references_button_generic_ajax_form.html"
                )
            super().__init__(data, *args, **kwargs)

        def render_other_prop(self, record):
            """
            displays the correct name direction of the related property with respect to main entity

            :param record: the current triple instance
            :return: related property name
            """

            # TODO: Make the related properties clickable (like it was in vanilla).
            if str(record.subj.pk) == model_self_id_str:
                return record.prop.name
            elif str(record.obj.pk) == model_self_id_str:
                return record.prop.name_reverse
            else:
                raise Exception(
                    "Did not find the entity this relation is supposed to come from!"
                    + "Something must have went wrong when annotating for the related instance."
                )

        def render_other_entity(self, record):
            """
            displays the other entity for each row

            :param record: the current triple instance
            :return: related instance
            """

            # TODO: Make the related entities clickable (like it was in vanilla).
            if str(record.subj.pk) == model_self_id_str:
                return record.obj
            elif str(record.obj.pk) == model_self_id_str:
                return record.subj
            else:
                raise Exception(
                    "Did not find the entity this relation is supposed to come from!"
                    + "Something must have went wrong when annotating for the related instance."
                )

        def render_edit(self, record):
            """
            renders the html for the button and injects the record pk into ajax call

            :param record: triple instance
            :return: rendered html button
            """

            return format_html(
                f"""
                    <a class='reledit' onclick="ajax_2_load_triple_form(div_origin=this, triple_id={record.pk})">
                    <svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" class="feather feather-edit-2">
                        <polygon points="16 3 21 8 8 21 3 21 3 16 16 3"></polygon>
                    </svg>
                </a>
            """
            )

        def render_delete(self, record):
            """
            renders the html for the button and injects the record pk into ajax call

            :param record: triple instance
            :return: rendered html button
            """

            return format_html(
                f"""
                <a class='reledit' onclick="ajax_2_delete_triple(div_origin=this, triple_id={record.id})">
                    <svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" class="feather feather-trash">
                        <polyline points="3 6 5 6 21 6">
                        </polyline>
                        <path d="M19 6v14a2 2 0 0 1-2 2H7a2 2 0 0 1-2-2V6m3 0V4a2 2 0 0 1 2-2h4a2 2 0 0 1 2 2v2">
                        </path>
                    </svg>
                </a>
            """
            )

    return render_to_string(
        request=request,
        template_name=TripleTable.Meta.template_name_custom,
        context={"table": TripleTable()},
    )


def render_reification_table(
    model_self_class_str,
    reification_type_str,
    model_self_id_str,
    should_be_editable,
    request,
):
    """
    renders the table of related reifications plus their related entities. To be used for a quick
    overview in an entity detail or edit view. Also, if needed with ajax calls prepared and
    integrated into the rows for edit and delete purpose.

    :param model_self_class_str: str representation of the main entity class, always referred as
    self, in django's lowercase format
    :param reification_type_str: str representation of the reification class, always referred as
    self, in django's lowercase format
    :param model_self_id_str: the id of the main entity instance, needed for creating triples
    :param should_be_editable: toggle if this should be rendered with edit buttons or not (for
    entity detail and edit view separately)
    :param request: the request object, needed for the table for whatever reason. Could not leave
    it out.
    :return: a html rendered string to be integrated into the calling view
    """

    reification_class = caching.get_reification_class_of_name(reification_type_str)
    model_self_class = caching.get_entity_class_of_name(model_self_class_str)
    model_self_instance = model_self_class.objects.get(pk=model_self_id_str)

    class ReificationTable(tables.Table):
        relation_type = tables.Column(empty_values=())
        related_entities = tables.Column(empty_values=())
        if should_be_editable:
            # It needs empty_values=(), otherwise the button icons would only render on the second
            # call. No idea why.
            edit = tables.Column(empty_values=())
            delete = tables.Column(empty_values=())

        class Meta:
            model = reification_class
            fields = ["relation_type", "related_entities"]
            if should_be_editable:
                fields += ["edit", "delete"]
            # If I would use `template_name` here, django-tables crashes. Perhaps it only expects
            # some of its own pre-integrated templates? But since we want to use a custom one and
            # also attach it to this class I renamed it to `template_name_custom`. I did not find a
            # better solution quickly.
            template_name_custom = "apis_relations/reification_table.html"

        def __init__(self, *args, **kwargs):
            super().__init__(
                *args,
                **kwargs,
                data=reification_class.objects.filter(
                    Q(triple_set_from_subj__obj=model_self_instance)
                    | Q(triple_set_from_obj__subj=model_self_instance)
                ).distinct(),
            )

        def render_relation_type(self, record):
            related_properties = []
            for triple in Triple.objects.filter(Q(subj=record) | Q(obj=record)):
                if triple.subj == model_self_instance and triple.obj == record:
                    related_properties.append(triple.prop.name)
                elif triple.obj == model_self_instance and triple.subj == record:
                    related_properties.append(triple.prop.name_reverse)
            related_properties = ", ".join(p for p in related_properties)
            return format_html(related_properties)

        def render_related_entities(self, record):
            """
            this method iterates over all entities that are:
            1. related to the reification of the current row
            2. are not the entity self which is the main entity we are viewing

            :param record: the reification instance, passed by the django-tables' logic
            :return: a html string containing all related entities to be displayed in a row
            """

            # TODO: Make the related entities clickable (like it was in vanilla).
            # note that this would also require a differentiation between detail and edit linking
            related_other_entities = []
            for triple in Triple.objects.filter(Q(subj=record) | Q(obj=record)):
                if triple.subj != record and triple.subj != model_self_instance:
                    related_other_entities.append(triple.subj)
                elif triple.obj != record and triple.obj != model_self_instance:
                    related_other_entities.append(triple.obj)
            related_other_entities = ", ".join([e.name for e in related_other_entities])
            return format_html(related_other_entities)

        def render_edit(self, record):
            """
            This renders a button that calls ajax logic to load the record reification into a form.

            Usually it's cleaner to avoid html code here in the python module and keep it with other
            templates, but rendering it here has the advantage of having access to the reification
            as full python object. Right now we only use its id, but should we need more elaborate
            logic the record python object here would come in handy.

            :param record: the reification instance, passed by the django-tables' logic
            :return: a html button
            """

            return format_html(
                f"""
                    <a class='reledit' onclick="ajax_2_load_reification_form(div_origin=this, reification_id={record.id})">
                    <svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" class="feather feather-edit-2">
                        <polygon points="16 3 21 8 8 21 3 21 3 16 16 3"></polygon>
                    </svg>
                </a>
            """
            )

        def render_delete(self, record):
            """
            This renders a button that calls ajax logic to delete the record reification.

            Usually it's cleaner to avoid html code here in the python module and keep it with other
            templates, but rendering it here has the advantage of having access to the reification
            as full python object. Right now we only use its id, but should we need more elaborate
            logic the record python object here would come in handy.

            :param record: the reification instance, passed by the django-tables' logic
            :return: a html button
            """
            return format_html(
                f"""
                <a class='reledit' onclick="ajax_2_delete_reification(div_origin=this, reification_id={record.id})">
                    <svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" class="feather feather-trash">
                        <polyline points="3 6 5 6 21 6">
                        </polyline>
                        <path d="M19 6v14a2 2 0 0 1-2 2H7a2 2 0 0 1-2-2V6m3 0V4a2 2 0 0 1 2-2h4a2 2 0 0 1 2 2v2">
                        </path>
                    </svg>
                </a>
            """
            )

    return render_to_string(
        request=request,
        template_name=ReificationTable.Meta.template_name_custom,
        context={"table": ReificationTable()},
    )


# TODO RDF: Check if this should be removed or adapted
class EntityUriTable(tables.Table):

    delete = tables.TemplateColumn(
        template_name="apis_relations/delete_button_Uri_ajax_form.html"
    )

    class Meta:
        empty_text = empty_text_default
        model = Uri
        fields = ["uri"]
        sequence = ("delete", "uri")
        # add class="paleblue" to <table> tag
        attrs = {
            "class": "table table-hover table-striped table-condensed",
            "id": "PURI_conn",
        }


# TODO RDF: Check if this should be removed or adapted
class LabelTableBase(tables.Table):

    label2 = tables.TemplateColumn(template_name="apis_relations/labels_label.html")

    # reuse the logic for ordering and rendering *_date_written
    # Important: The names of these class variables must correspond to the column field name,
    # e.g. for start_date_written, the methods must be named order_start_date_written and render_start_date_written
    order_start_date_written = generic_order_start_date_written
    order_end_date_written = generic_order_end_date_written
    render_start_date_written = generic_render_start_date_written
    render_end_date_written = generic_render_end_date_written

    class Meta:

        empty_text = empty_text_default
        model = Label

        # Note that as the next attribute 'sequence' builds on this list 'fields', the order defined within this list
        # will be reused for the tuple 'sequence'. So if the order needs to be changed, better do it here in the list 'fields'.
        fields = [
            "start_date_written",
            "end_date_written",
            "label_type",
            "isoCode_639_3",
        ]
        sequence = ("label2",) + tuple(fields)

        # add class="paleblue" to <table> tag
        attrs = {
            "class": "table table-hover table-striped table-condensed",
            "id": "PL_conn",
        }


# TODO RDF: Check if this should be removed or adapted
class LabelTableEdit(LabelTableBase):
    """
    Reuse most of the base table class for labels. Only addition is editing functionality.
    """

    edit = tables.TemplateColumn(
        template_name="apis_relations/edit_button_persLabel_ajax_form.html"
    )

    class Meta(LabelTableBase.Meta):
        sequence = LabelTableBase.Meta.sequence + ("edit",)
