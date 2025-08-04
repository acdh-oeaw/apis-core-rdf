import django_tables2 as tables
from django.apps import apps

from apis_core.generic.tables import ActionColumn, CustomTemplateColumn, ViewColumn


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
    verbose_name = "Original ID"


class ResetColumn(ActionColumn):
    """
    A column showing a reset button
    """

    template_name = "history/columns/reset.html"
    permission = "change"


class APISHistoryTableBaseTable(tables.Table):
    history_id = tables.Column(verbose_name="ID")
    original_id = OriginalIDColumn()
    desc = DescriptionColumnHistory()
    view = ViewColumn()

    class Meta:
        fields = ["history_id", "desc", "most_recent", "view"]


class HistoryGenericTable(tables.Table):
    model = tables.Column(empty_values=())
    fields_changed = tables.Column(empty_values=())
    instance = tables.Column(linkify=lambda record: record.get_absolute_url())
    fields_changed = tables.TemplateColumn(
        template_name="history/columns/fields_changed.html"
    )
    reset = ResetColumn()

    class Meta:
        fields = [
            "model",
            "instance",
            "fields_changed",
            "history_type",
            "history_date",
            "history_user",
        ]

    def render_model(self, record):
        return record.instance.__class__.__name__

    def __init__(self, *args, **kwargs):
        print(kwargs)
        if apps.is_installed("apis_core.collections"):
            from apis_core.collections.columns import CollectionsColumn

            kwargs["extra_columns"] = [("collections", CollectionsColumn())]
        super().__init__(*args, **kwargs)
