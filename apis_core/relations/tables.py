import django_tables2 as tables

from django.contrib.contenttypes.models import ContentType

from .models import Relation


class RelationTable(tables.Table):

    id = tables.TemplateColumn(
            "<a href='{% url 'apis:relationupdate' record.id %}'>{{ record.id }}</a>"
    )

    description = tables.TemplateColumn("{{ record }}")
    edit = tables.TemplateColumn(
            "<a href='{% url 'apis:relationupdate' record.id %}'>Edit</a>"
    )
    delete = tables.TemplateColumn(template_name="tables/delete.html")

    class Meta:
        model = Relation
        fields = ["id", "description", "edit"]
        sequence = tuple(fields)
