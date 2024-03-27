from apis_core.generic.tables import CustomTemplateColumn, ViewColumn
import django_tables2 as tables


class DescriptionColumnHistory(CustomTemplateColumn):
    """
    A column showing a model description
    """

    template_name = "history/columns/description.html"
    orderable = False


class OriginalIDColumn(CustomTemplateColumn):
    """
    A column showing the original id of a model instance
    """

    template_name = "history/columns/original_id.html"
    orderable = False
    verbose_name = "most recent"


class APISHistoryTableBaseTable(tables.Table):
    history_id = tables.Column(verbose_name="ID")
    most_recent = OriginalIDColumn()
    desc = DescriptionColumnHistory()
    view = ViewColumn()

    class Meta:
        fields = ["history_id", "desc", "most_recent", "view"]
