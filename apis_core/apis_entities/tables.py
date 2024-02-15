from apis_core.generic.helpers import permission_fullname
from apis_core.generic.tables import GenericTable, ActionColumn


class DuplicateColumn(ActionColumn):
    """
    A column showing a view button
    """

    template_name = "columns/duplicate.html"


class AbstractEntityTable(GenericTable):
    noduplicate = DuplicateColumn()

    class Meta(GenericTable.Meta):
        sequence = ("...", "view", "edit", "noduplicate", "delete")

    def before_render(self, request):
        super().before_render(request)
        if model := getattr(self.Meta, "model"):
            if not request.user.has_perm(permission_fullname("create", model)):
                self.columns.hide("noduplicate")
