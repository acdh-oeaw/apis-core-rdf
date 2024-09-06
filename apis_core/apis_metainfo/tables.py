import django_tables2 as tables
from django.db.models import F

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
        verbose_name="Entity Type",
    )

    class Meta(GenericTable.Meta):
        model = Uri
        fields = ["id", "uri", "entity", "ent_type"]
        exclude = ("desc",)

    def order_ent_type(self, queryset, is_descending):
        queryset = queryset.annotate(
            ent_type=F("root_object__self_contenttype__model")
        ).order_by(("-" if is_descending else "") + "ent_type")
        return (queryset, True)
