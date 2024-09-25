import django_tables2 as tables
from django.conf import settings
from django.db.models import Case, F, When
from django.utils.html import format_html

from apis_core.apis_relations.models import TempTriple
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
        kwargs["linkify_item"] = lambda record: record.model_class().get_listview_url()
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


class TripleTableBase(GenericTable):
    """
    The base table from which detail or edit tables will inherit from in order to avoid redundant definitions
    """

    class Meta:
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

    def order_start_date_written(self, queryset, is_descending):
        if is_descending:
            return (queryset.order_by(F("start_date").desc(nulls_last=True)), True)
        return (queryset.order_by(F("start_date").asc(nulls_last=True)), True)

    def order_end_date_written(self, queryset, is_descending):
        if is_descending:
            return (queryset.order_by(F("end_date").desc(nulls_last=True)), True)
        return (queryset.order_by(F("end_date").asc(nulls_last=True)), True)

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
                When(**{"subj__pk": self.entity_pk_self, "then": "obj"}),
                When(**{"obj__pk": self.entity_pk_self, "then": "subj"}),
            ),
            other_prop=Case(
                # **kwargs pattern is needed here as the key-value pairs change with each relation class and entity instance.
                When(**{"subj__pk": self.entity_pk_self, "then": "prop__name_forward"}),
                When(**{"obj__pk": self.entity_pk_self, "then": "prop__name_reverse"}),
            ),
        )

        self.base_columns["other_prop"].verbose_name = "Other property"
        self.base_columns[
            "other_entity"
        ].verbose_name = f"Related {self.other_entity_class_name.title()}"

        super().__init__(data, *args, **kwargs)

    def render_start_date_written(self, record, value):
        if record.start_start_date is not None and record.start_end_date is not None:
            title_text = f"{record.start_start_date} - {record.start_end_date}"
        elif record.start_date is not None:
            title_text = record.start_date
        else:
            return "—"
        return format_html(f"<abbr title='{title_text}'>{value}</b>")

    def render_end_date_written(self, record, value):
        if record.end_start_date is not None and record.end_end_date is not None:
            title_text = f"{record.end_start_date} - {record.end_end_date}"
        elif record.end_date is not None:
            title_text = record.end_date
        else:
            return "—"
        return format_html(f"<abbr title='{title_text}'>{value}</b>")


class TripleTableDetail(TripleTableBase):
    class Meta(TripleTableBase.Meta):
        exclude = TripleTableBase.Meta.exclude + ("delete", "edit")

    def __init__(self, data, *args, **kwargs):
        self.base_columns["other_entity"] = tables.Column(
            linkify=lambda record: record.obj.get_absolute_url()
            if record.other_entity == record.obj.id
            else record.subj.get_absolute_url()
        )

        # bibsonomy button
        if "apis_bibsonomy" in settings.INSTALLED_APPS:
            self.base_columns["ref"] = tables.TemplateColumn(
                template_name="apis_relations/references_button_generic_ajax_form.html"
            )

        super().__init__(data=data, *args, **kwargs)


class TripleTableEdit(TripleTableBase):
    class Meta(TripleTableBase.Meta):
        fields = TripleTableBase.Meta.fields
        if "apis_bibsonomy" in settings.INSTALLED_APPS:
            fields = ["ref"] + TripleTableBase.Meta.fields
        sequence = tuple(fields)

    def __init__(self, *args, **kwargs):
        self.base_columns["other_entity"] = tables.Column(
            linkify=lambda record: record.obj.get_edit_url()
            if record.other_entity == record.obj.id
            else record.subj.get_edit_url()
        )

        self.base_columns["edit"] = tables.TemplateColumn(
            template_name="apis_relations/edit_button_generic_ajax_form.html"
        )

        if "apis_bibsonomy" in settings.INSTALLED_APPS:
            self.base_columns["ref"] = tables.TemplateColumn(
                template_name="apis_relations/references_button_generic_ajax_form.html"
            )

        super().__init__(*args, **kwargs)


def get_generic_triple_table(other_entity_class_name, entity_pk_self, detail):
    if detail:
        tt = TripleTableDetail
    else:
        tt = TripleTableEdit
    tt.entity_pk_self = entity_pk_self
    tt.other_entity_class_name = other_entity_class_name
    return tt
