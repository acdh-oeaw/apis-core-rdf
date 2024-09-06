from apis_core.generic.tables import CustomTemplateColumn, GenericTable


class RelationColumn(CustomTemplateColumn):
    template_name = "columns/relation.html"
    verbose_name = ""


class RelationsListTable(GenericTable):
    relation = RelationColumn()

    class Meta:
        attrs = {"class": "table-sm"}
        sequence = GenericTable.Meta.sequence
        exclude = ("desc",)
