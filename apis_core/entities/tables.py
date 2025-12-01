from django_tables2 import TemplateColumn

from apis_core.generic.tables import GenericTable


class EntityIDTable(GenericTable):
    target = TemplateColumn(
        "<a href='{{ record.content_object.get_absolute_url }}'>{{ record.content_object }}</a>",
        orderable=False,
    )
    canonical_url = TemplateColumn(
        "<a href='{{ record.content_object.get_canonical_url }}'>{{ record.content_object.get_canonical_url }}</a>",
        orderable=False,
    )

    class Meta(GenericTable.Meta):
        exclude = ("desc",)
