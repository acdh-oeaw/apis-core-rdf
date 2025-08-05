import django_tables2 as tables

from apis_core.generic.tables import GenericTable

from .models import Uri


class UriTable(GenericTable):
    entity = tables.TemplateColumn(
        "<a href='{{ record.content_object.get_absolute_url }}'>{{ record.content_object }}</a>",
        orderable=False,
        verbose_name="related Entity",
    )
    content_type = tables.TemplateColumn(
        "{{ record.content_type.model }}",
        verbose_name="Entity Type",
    )

    class Meta(GenericTable.Meta):
        model = Uri
        fields = ["id", "uri", "entity", "content_type"]
        exclude = ("desc",)
