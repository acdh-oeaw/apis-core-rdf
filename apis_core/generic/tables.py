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


class DeleteColumn(CustomTemplateColumn):
    """
    A column showing a delete button
    """

    template_name = "columns/delete.html"
    orderable = False
    exclude_from_export = True
    verbose_name = ""
    attrs = {"td": {"style": "width:1%;"}}


class EditColumn(CustomTemplateColumn):
    """
    A column showing an edit button
    """

    template_name = "columns/edit.html"
    orderable = False
    exclude_from_export = True
    verbose_name = ""
    attrs = {"td": {"style": "width:1%;"}}


class ViewColumn(CustomTemplateColumn):
    """
    A column showing a view button
    """

    template_name = "columns/view.html"
    orderable = False
    exclude_from_export = True
    verbose_name = ""
    attrs = {"td": {"style": "width:1%;"}}


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

    def __init__(self, *args, **kwargs):
        # if there is no custom sequence set, move `edit` and `delete` to the back
        if "sequence" not in kwargs:
            kwargs["sequence"] = ["...", "view", "edit", "delete"]

        super().__init__(*args, **kwargs)

    def before_render(self, request):
        if model := getattr(self.Meta, "model"):
            if not request.user.has_perm(permission_fullname("delete", model)):
                self.columns.hide("delete")
            if not request.user.has_perm(permission_fullname("edit", model)):
                self.columns.hide("edit")
            if not request.user.has_perm(permission_fullname("view", model)):
                self.columns.hide("view")
