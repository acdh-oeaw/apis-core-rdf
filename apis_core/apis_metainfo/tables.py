import django_tables2 as tables
from django.utils.html import format_html
from apis_core.generic.tables import GenericTable

from .models import Uri


def helper_render_date(value, var_date, var_start_date, var_end_date):
    """
    helper function to avoid duplicated code. It checks the various sub-dates of a model's date field for them being None
    or having values. If a field is None then check for the next, and if all are None, return '—' inditcating no value.

    If there are values, use them as mouse overlay helptext to inform the user about the parsing result behind a written
    date field.

    :param value: str : the \*_date_written (either start_date_written or end_date_written) field of an entity or relation
    :param var_date: datetime : either the precisely parsed date or the average in between two dates when \*_date_written is a range
    :param var_start_date: datetime : The sub-date of var_date, indicating the start date of the range
    :param var_end_date: datetime : The sub-date of var_date, indicating the end date of the range
    :return: html string : which has the value of the written date and the parsed dates as mouse overlay helptext
    """

    # Various if-else branches checking which of the date fields are not None and should be used

    if var_start_date is not None and var_end_date is not None:
        overlay_help_text = str(var_start_date) + " - " + str(var_end_date)

    elif var_date is not None:
        overlay_help_text = str(var_date)

    else:
        return "—"

    return format_html("<abbr title='" + overlay_help_text + "'>" + value + "</b>")


# Again this function serves a generic purpose and must be assigned as class method to django-tables2 tables.Table class
# The whole logic is very similare to the generic_order_* functions above, so see their comments for more details.
def generic_render_start_date_written(self, record, value):
    return helper_render_date(
        value=value,
        var_date=record.start_date,
        var_start_date=record.start_start_date,
        var_end_date=record.start_end_date,
    )


def generic_render_end_date_written(self, record, value):
    return helper_render_date(
        value=value,
        var_date=record.end_date,
        var_start_date=record.end_start_date,
        var_end_date=record.end_end_date,
    )


class UriTable(GenericTable):
    entity = tables.TemplateColumn(
        "<a href='{{ record.root_object.get_absolute_url }}'>{{ record.root_object }}</a>",
        orderable=True,
        verbose_name="related Entity",
    )
    ent_type = tables.TemplateColumn(
        "{{ record.root_object.self_contenttype.model }}",
        orderable=False,
        verbose_name="Entity Type",
    )

    class Meta(GenericTable.Meta):
        model = Uri
        fields = ["id", "desc", "entity", "ent_type"]
