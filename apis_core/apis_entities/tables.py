from apis_core.generic.tables import GenericTable, ActionColumn
from apis_core.generic.helpers import permission_fullname


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

    def before_render(self, request):
        super().before_render(request)
        if model := getattr(self.Meta, "model"):
            if not request.user.has_perm(permission_fullname("create", model)):
                self.columns.hide("noduplicate")
