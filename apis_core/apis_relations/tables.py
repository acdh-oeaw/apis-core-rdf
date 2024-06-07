import django_tables2 as tables
from django.conf import settings
from django.db.models import Case, When, F
from django.utils.html import format_html
from django_tables2.utils import A

from apis_core.apis_metainfo.tables import (
    generic_order_start_date_written,
    generic_order_end_date_written,
    generic_render_start_date_written,
    generic_render_end_date_written,
)
from apis_core.generic.tables import GenericTable

empty_text_default = "There are currently no relations"


class TripleTable(GenericTable):
    subj = tables.Column(linkify=True)
    obj = tables.Column(linkify=True)

    class Meta(GenericTable.Meta):
        fields = ["id", "subj", "prop", "obj"]
        exclude = ["desc"]
        sequence = tuple(fields) + GenericTable.Meta.sequence


class SubjObjColumn(tables.ManyToManyColumn):
    def __init__(self, *args, **kwargs):
        kwargs["separator"] = format_html(",<br>")
        kwargs["orderable"] = True
        kwargs["filter"] = lambda qs: qs.order_by("model")
        kwargs["transform"] = lambda ent: f"{ent.name.capitalize()}"
        kwargs["linkify_item"] = {
            "viewname": "apis_core:apis_entities:generic_entities_list",
            "args": [tables.A("model")],
        }
        super().__init__(*args, **kwargs)


class PropertyTable(GenericTable):
    """Construct table for properties.

    The table shows how entities connect with one another via properties (relations).
    It uses the format of an RDF triple – Subject-Predicate-Object – plus
    "Reverse Predicate" for the inverse relationship and is displayed on the frontend
     on the Relations > Property page.
    """

    # Note on constructing table columns / usage of variables:
    # The variables used to declare table columns need to have the same names
    # as the model field names from which the columns should be created,
    # or tables.Column needs to contain an attribute "accessor" which references
    # the original field name.
    # For columns which allow sorting, the variable names are used as sort strings
    # in the user's browser address bar, so for UX reasons, it may make sense to
    # use different variable names than the original field names.

    predicate = tables.Column(accessor="name_forward", verbose_name="Predicate")
    predicate_reverse = tables.Column(
        accessor="name_reverse", verbose_name="Reverse predicate"
    )
    subject = SubjObjColumn(accessor="subj_class", verbose_name="Subject")
    object = SubjObjColumn(accessor="obj_class", verbose_name="Object")

    class Meta(GenericTable.Meta):
        fields = ["subject", "predicate", "object", "predicate_reverse"]
        order_by = "predicate"
        exclude = ["desc"]
        sequence = tuple(fields) + GenericTable.Meta.sequence

    # Use order_ methods to define how individual columns should be sorted.
    # Method names are column names prefixed with "order_".
    # By default, columns for regular fields are sorted alphabetically; for
    # ManyToMany fields, however, the row IDs of the originating table are
    # used as basis for sorting.
    # When column names and field names differ (see earlier note), the original
    # field names need to be referenced when constructing queryset.
    def order_subject(self, queryset, is_descending):
        queryset = queryset.annotate(entity=F("subj_class__model")).order_by(
            ("-" if is_descending else "") + "entity"
        )
        return (queryset, True)

    def order_object(self, queryset, is_descending):
        queryset = queryset.annotate(entity=F("obj_class__model")).order_by(
            ("-" if is_descending else "") + "entity"
        )
        return (queryset, True)


def get_generic_triple_table(other_entity_class_name, entity_pk_self, detail):
    # TODO RDF : add code from before refactoring and comment it out
    class TripleTableBase(GenericTable):
        """
        The base table from which detail or edit tables will inherit from in order to avoid redundant definitions
        """

        # reuse the logic for ordering and rendering *_date_written
        # Important: The names of these class variables must correspond to the column field name,
        # e.g. for start_date_written, the methods must be named order_start_date_written and render_start_date_written
        order_start_date_written = generic_order_start_date_written
        order_end_date_written = generic_order_end_date_written
        render_start_date_written = generic_render_start_date_written
        render_end_date_written = generic_render_end_date_written

        class Meta:
            from apis_core.apis_relations.models import TempTriple

            model = TempTriple

            # the fields list also serves as the defining order of them, as to avoid duplicated definitions
            fields = [
                "start_date_written",
                "end_date_written",
                "other_prop",
                "other_entity",
                "notes",
            ]
            exclude = (
                "desc",
                "view",
            )
            # reuse the list for ordering
            sequence = tuple(fields)

        def render_other_entity(self, record, value):
            """
            Custom render_FOO method for related entity linking. Since the 'other_related_entity' is a generated annotation
            on the queryset, it does not return the related instance but only the foreign key as the integer it is.
            Thus fetching the related instance is necessary.

            :param record: The 'row' of a queryset, i.e. an entity instance
            :param value: The current column of the row, i.e. the 'other_related_entity' annotation
            :return: related instance
            """

            if value == record.subj.pk:
                return record.subj

            elif value == record.obj.pk:
                return record.obj

            else:
                raise Exception(
                    "Did not find the entity this relation is supposed to come from!"
                    + "Something must have went wrong when annotating for the related instance."
                )

        def __init__(self, data, *args, **kwargs):
            data = data.annotate(
                other_entity=Case(
                    # **kwargs pattern is needed here as the key-value pairs change with each relation class and entity instance.
                    When(**{"subj__pk": entity_pk_self, "then": "obj"}),
                    When(**{"obj__pk": entity_pk_self, "then": "subj"}),
                ),
                other_prop=Case(
                    # **kwargs pattern is needed here as the key-value pairs change with each relation class and entity instance.
                    When(**{"subj__pk": entity_pk_self, "then": "prop__name_forward"}),
                    When(**{"obj__pk": entity_pk_self, "then": "prop__name_reverse"}),
                ),
            )

            self.base_columns["other_prop"].verbose_name = "Other property"
            self.base_columns[
                "other_entity"
            ].verbose_name = f"Related {other_entity_class_name.title()}"

            super().__init__(data, *args, **kwargs)

    if detail:

        class TripleTableDetail(TripleTableBase):
            """
            Sublcass inheriting the bulk of logic from parent. This table is used for the 'detail' views.
            """

            class Meta(TripleTableBase.Meta):
                exclude = TripleTableBase.Meta.exclude + ("delete", "edit")

            def __init__(self, data, *args, **kwargs):
                self.base_columns["other_entity"] = tables.LinkColumn(
                    "apis_core:apis_entities:generic_entities_detail_view",
                    args=[other_entity_class_name, A("other_entity")],
                )

                # bibsonomy button
                if "apis_bibsonomy" in settings.INSTALLED_APPS:
                    self.base_columns["ref"] = tables.TemplateColumn(
                        template_name="apis_relations/references_button_generic_ajax_form.html"
                    )

                super().__init__(data=data, *args, **kwargs)

        return TripleTableDetail

    else:

        class TripleTableEdit(TripleTableBase):
            """
            Sublcass inheriting the bulk of logic from parent. This table is used for the 'edit' view.
            """

            class Meta(TripleTableBase.Meta):
                fields = TripleTableBase.Meta.fields
                if "apis_bibsonomy" in settings.INSTALLED_APPS:
                    fields = ["ref"] + TripleTableBase.Meta.fields

                # again reuse the fields list for ordering
                sequence = tuple(fields)

            def __init__(self, *args, **kwargs):
                self.base_columns["other_entity"] = tables.LinkColumn(
                    "apis_core:apis_entities:generic_entities_edit_view",
                    args=[other_entity_class_name, A("other_entity")],
                )

                # edit button
                self.base_columns["edit"] = tables.TemplateColumn(
                    template_name="apis_relations/edit_button_generic_ajax_form.html"
                )

                # bibsonomy button
                if "apis_bibsonomy" in settings.INSTALLED_APPS:
                    self.base_columns["ref"] = tables.TemplateColumn(
                        template_name="apis_relations/references_button_generic_ajax_form.html"
                    )

                super().__init__(*args, **kwargs)

        return TripleTableEdit
