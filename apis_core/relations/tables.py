from apis_core.generic.tables import ActionsColumn, CustomTemplateColumn, GenericTable


class RelationActionsColumn(ActionsColumn):
    template_name = "columns/relation_actions.html"


class RelationColumn(CustomTemplateColumn):
    template_name = "columns/relation.html"
    verbose_name = ""


class RelationsListTable(GenericTable):
    relation = RelationColumn()
    actions = RelationActionsColumn()

    class Meta:
        attrs = {"class": "table-sm"}
        sequence = GenericTable.Meta.sequence
        exclude = ("desc",)
