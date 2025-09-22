from apis_core.generic.tables import ActionColumn, GenericTable


class DuplicateColumn(ActionColumn):
    """
    A column showing a duplicate button
    """

    template_name = "columns/duplicate.html"
    permission = "create"
    verbose_name = "duplicate"


class AbstractEntityTable(GenericTable):
    noduplicate = DuplicateColumn()

    class Meta(GenericTable.Meta):
        sequence = ("...", "view", "edit", "delete", "noduplicate")
