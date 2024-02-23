import django_tables2 as tables
from django.conf import settings
from django.db.models import F
from django.utils.html import format_html
from apis_core.apis_relations.models import TempTriple

from apis_core.generic.tables import GenericTable, CustomTemplateColumn


def helper_render_date(value, var_date, var_start_date, var_end_date):
    """
    helper function to avoid duplicated code. It checks the various sub-dates of a model's date field for them being None
    or having values. If a field is None then check for the next, and if all are None, return '—' inditcating no value.

    If there are values, use them as mouse overlay helptext to inform the user about the parsing result behind a written
    date field.

    :param value: str : the *_date_written (either start_date_written or end_date_written) field of an entity or relation
    :param var_date: datetime : either the precisely parsed date or the average in between two dates when *_date_written is a range
    :param var_start_date: datetime : The sub-date of var_date, indicating the start date of the range
    :param var_end_date: datetime : The sub-date of var_date, indicating the end date of the range
    :return: html string : which has the value of the written date and the parsed dates as mouse overlay helptext
    """
    if var_start_date is not None and var_end_date is not None:
        overlay_help_text = str(var_start_date) + " - " + str(var_end_date)
    elif var_date is not None:
        overlay_help_text = str(var_date)
    else:
        return "—"
    return format_html("<abbr title='" + overlay_help_text + "'>" + value + "</b>")


class StartDateColumn(tables.Column):
    def order(self, queryset, is_descending):
        if is_descending:
            queryset = queryset.order_by(F("start_date").desc(nulls_last=True))
        else:
            queryset = queryset.order_by(F("start_date").asc(nulls_last=True))
        return (queryset, True)

    def render(self, record, value):
        return helper_render_date(
            value=value,
            var_date=record.start_date,
            var_start_date=record.start_start_date,
            var_end_date=record.start_end_date,
        )


class EndDateColumn(tables.Column):
    def order(self, queryset, is_descending):
        if is_descending:
            queryset = queryset.order_by(F("end_date").desc(nulls_last=True))
        else:
            queryset = queryset.order_by(F("end_date").asc(nulls_last=True))
        return (queryset, True)

    def render(self, record, value):
        return helper_render_date(
            value=value,
            var_date=record.end_date,
            var_start_date=record.end_start_date,
            var_end_date=record.end_end_date,
        )


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


class AjaxEditColumn(CustomTemplateColumn):
    orderable = False
    exclude_from_export = True
    verbose_name = ""
    template_name = "apis_relations/edit_button_generic_ajax_form.html"


class AjaxDeleteColumn(CustomTemplateColumn):
    orderable = False
    exclude_from_export = True
    verbose_name = ""
    template_name = "apis_relations/delete_button_generic_ajax_form.html"


class AjaxBibsonomyColumn(CustomTemplateColumn):
    orderable = False
    exclude_from_export = True
    verbose_name = ""
    template_name = "apis_relations/references_button_generic_ajax_form.html"


class TripleTable(GenericTable):
    subj = tables.Column(linkify=True)
    obj = tables.Column(linkify=True)

    class Meta:
        fields = ["id", "subj", "prop", "obj"]
        exclude = ["desc"]
        sequence = ("id", "subj", "prop", "obj", "...")


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

    class Meta:
        fields = ["subject", "predicate", "object", "predicate_reverse"]
        order_by = "predicate"
        exclude = ["desc"]

    def __init__(self, *args, **kwargs):
        if "sequence" not in kwargs:
            kwargs["sequence"] = [
                "subject",
                "predicate",
                "object",
                "predicate_reverse",
                "...",
            ]
        super().__init__(*args, **kwargs)

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


class TempTripleDetailTable(GenericTable):
    start_date_written = StartDateColumn(attrs={"td": {"class": "col-md-1"}})
    end_date_written = EndDateColumn(attrs={"td": {"class": "col-md-1"}})
    prop = tables.Column(
        verbose_name="Relation type", attrs={"td": {"class": "col-md-2"}}
    )
    subj = tables.Column(linkify=True, attrs={"td": {"class": "col-md-5"}})
    obj = tables.Column(linkify=True, attrs={"td": {"class": "col-md-5"}})
    forward = True

    class Meta:
        model = TempTriple
        fields = [
            "start_date_written",
            "end_date_written",
            "prop",
            "obj",
            "subj",
            "notes",
        ]
        exclude = ["desc", "view", "delete", "edit"]
        sequence = tuple(fields)

    def __init__(self, data, instance=None, *args, **kwargs):
        if data:
            subj = data.first().subj
            self.base_columns[
                "subj"
            ].verbose_name = f"Relation {subj._meta.verbose_name}"
            obj = data.first().obj
            self.base_columns["obj"].verbose_name = f"Related {obj._meta.verbose_name}"
            if subj.id != getattr(instance, "id", None):
                self.forward = False
        super().__init__(data, *args, **kwargs)

    def before_render(self, request):
        if self.forward:
            self.columns.hide("subj")
        else:
            self.columns.hide("obj")

    def render_prop(self, record):
        if not self.forward:
            return record.prop.name_reverse
        return record.prop.name_forward


TempTripleDetailTablePagination = {"per_page": 20}


class TempTripleEditTable(TempTripleDetailTable):
    ajedit = AjaxEditColumn()
    ajdelete = AjaxDeleteColumn()

    class Meta(TempTripleDetailTable.Meta):
        fields = TempTripleDetailTable.Meta.fields
        exclude = ["edit", "delete", "view"]
        if "apis_bibsonomy" in settings.INSTALLED_APPS:
            fields = ["ref"] + fields
        sequence = tuple(fields) + tuple(["..."])
