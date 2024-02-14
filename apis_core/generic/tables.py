import django_tables2 as tables
from apis_core.generic.helpers import permission_fullname


class CustomTemplateColumn(tables.TemplateColumn):
    """
    A custom template column - the `tables.TemplateColumn` class does not allow
    to set attributes via class variables. Therefor we use this
    CustomTemplateColumn to set some arguments based on class attributes and
    override the attributes in child classes.
    """

    template_name = None
    orderable = None
    exclude_from_export = False
    verbose_name = None

    def __init__(self, *args, **kwargs):
        super().__init__(
            template_name=self.template_name,
            orderable=self.orderable,
            exclude_from_export=self.exclude_from_export,
            verbose_name=self.verbose_name,
            *args,
            **kwargs,
        )


class ActionColumn(CustomTemplateColumn):
    """
    A custom template column with some additional attributes
    for actions.
    """

    orderable = False
    exclude_from_export = True
    verbose_name = ""
    attrs = {"td": {"style": "width:1%;"}}


class DeleteColumn(ActionColumn):
    """
    A column showing a delete button
    """

    template_name = "columns/delete.html"


class EditColumn(ActionColumn):
    """
    A column showing an edit button
    """

    template_name = "columns/edit.html"


class ViewColumn(ActionColumn):
    """
    A column showing a view button
    """

    template_name = "columns/view.html"


class DescriptionColumn(CustomTemplateColumn):
    """
    A column showing a model description
    """

    template_name = "columns/description.html"
    orderable = False


class GenericTable(tables.Table):
    """
    A generic table that contains an edit button column, a delete button column
    and a description column
    """

    edit = EditColumn()
    desc = DescriptionColumn()
    delete = DeleteColumn()
    view = ViewColumn()

    class Meta:
        fields = ["id", "desc"]
        sequence = ("...", "view", "edit", "delete")

    def before_render(self, request):
        if model := getattr(self.Meta, "model"):
            if not request.user.has_perm(permission_fullname("delete", model)):
                self.columns.hide("delete")
            if not request.user.has_perm(permission_fullname("change", model)):
                self.columns.hide("edit")
            if not request.user.has_perm(permission_fullname("view", model)):
                self.columns.hide("view")
