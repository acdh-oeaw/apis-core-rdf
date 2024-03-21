import django_tables2 as tables
from apis_core.generic.tables import GenericTable

from .models import Uri


class UriTable(GenericTable):
    entity = tables.TemplateColumn(
        "<a href='{{ record.root_object.get_absolute_url }}'>{{ record.root_object }}</a>",
        orderable=True,
        verbose_name="related Entity",
    )
    ent_type = tables.TemplateColumn(
        "{{ record.root_object.self_contenttype.model }}",
        orderable=False,
        verbose_name="Entity Type",
    )

    class Meta(GenericTable.Meta):
        model = Uri
        fields = ["id", "desc", "entity", "ent_type"]
