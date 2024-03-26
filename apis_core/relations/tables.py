import django_tables2 as tables
from django.template.loader import get_template
from apis_core.generic.tables import GenericTable


class GenericRelationsTable(GenericTable):
    prop = tables.Column(empty_values=())
    related_instance = tables.Column(empty_values=())

    class Meta(GenericTable.Meta):
        exclude = ["desc"]

    def __init__(self, data, instance, *args, **kwargs):
        self.instance = instance
        return super().__init__(data, *args, **kwargs)

    def render_prop(self, record):
        if record.subj_inheritance == self.instance:
            return record.name
        return record.reverse_name

    def render_related_instance(self, record):
        template = get_template("relations/columns/link_to_absolute_url.html")
        if record.subj_inheritance == self.instance:
            return template.render({"record": record.obj_inheritance})
        return template.render({"record": record.subj_inheritance})
