from apis_core.generic.tables import GenericTable, ActionColumn


class DuplicateColumn(ActionColumn):
    """
    A column showing a view button
    """

    template_name = "columns/duplicate.html"
    permission = "create"


class AbstractEntityTable(GenericTable):
    noduplicate = DuplicateColumn()

    class Meta(GenericTable.Meta):
        sequence = ("...", "view", "edit", "delete", "noduplicate")
