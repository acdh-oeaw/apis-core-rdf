from apis_core.generic.tables import GenericTable


class RelationsListTable(GenericTable):
    class Meta:
        attrs = {"class": "table-sm"}
        sequence = GenericTable.Meta.sequence

    def render_desc(self, record):
        if record.forward:
            return record.subj_to_obj_text
        return record.obj_to_subj_text
