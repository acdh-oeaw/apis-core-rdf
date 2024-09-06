from django_tables2 import TemplateColumn

from apis_core.generic.tables import GenericTable


class SkosCollectionContentObjectTable(GenericTable):
    target = TemplateColumn(
        "<a href='{{ record.content_object.get_absolute_url }}'>{{ record.content_object }}</a>",
        orderable=False,
    )
