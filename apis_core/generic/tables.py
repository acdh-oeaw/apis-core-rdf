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

    def render(self, record, table, *args, **kwargs):
        if permission := getattr(self, "permission", False):
            if not table.request.user.has_perm(permission_fullname(permission, record)):
                return ""
        return super().render(record, table, *args, **kwargs)


class DeleteColumn(ActionColumn):
    """
    A column showing a delete button
    """

    template_name = "columns/delete.html"
    permission = "delete"


class EditColumn(ActionColumn):
    """
    A column showing an edit button
    """

    template_name = "columns/edit.html"
    permission = "change"


class ViewColumn(ActionColumn):
    """
    A column showing a view button
    """

    template_name = "columns/view.html"
    permission = "view"


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


class MoreLessColumn(tables.TemplateColumn):
    """
    Useful for displaying long fields.
    A preview is shown initially with a "Show more" link
    which is replaced with a "Show less" link when expanded.
    """

    template_name = "columns/more-less.html"

    def __init__(self, preview, fulltext, *args, **kwargs):
        self.preview = preview
        self.fulltext = fulltext
        super().__init__(template_name=self.template_name, *args, **kwargs)

    def render(self, record, **kwargs):
        self.extra_context["preview"] = self.preview(record)
        self.extra_context["fulltext"] = self.fulltext(record)
        return super().render(record, **kwargs)
