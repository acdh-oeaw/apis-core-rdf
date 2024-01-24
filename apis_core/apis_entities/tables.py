from apis_core.generic.tables import GenericTable, ActionColumn


class DuplicateColumn(ActionColumn):
    """
    A column showing a view button
    """

    template_name = "columns/duplicate.html"


class AbstractEntityTable(GenericTable):
    noduplicate = DuplicateColumn()

    def __init__(self, *args, **kwargs):
        # if there is no custom sequence set, move `edit` and `delete` to the back
        if "sequence" not in kwargs:
            kwargs["sequence"] = ["...", "view", "edit", "noduplicate", "delete"]

        super().__init__(*args, **kwargs)
