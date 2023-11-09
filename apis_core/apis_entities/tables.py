import django_tables2 as tables
from django.utils.safestring import mark_safe
from django_tables2.utils import A
from apis_core.utils.settings import (
    list_links_to_edit,
    get_entity_settings_by_modelname,
)

from apis_core.apis_metainfo.tables import (
    generic_order_start_date_written,
    generic_order_end_date_written,
    generic_render_start_date_written,
    generic_render_end_date_written,
)
from apis_core.utils import caching


def get_entities_table(entity, default_cols):
    if default_cols is None:
        default_cols = [
            "name",
        ]

    class GenericEntitiesTable(tables.Table):
        def render_name(self, record, value):
            if value == "":
                return "(No name provided)"
            else:
                return value

        # reuse the logic for ordering and rendering *_date_written
        # Important: The names of these class variables must correspond to the column field name,
        # e.g. for start_date_written, the methods must be named order_start_date_written and render_start_date_written
        order_start_date_written = generic_order_start_date_written
        order_end_date_written = generic_order_end_date_written
        render_start_date_written = generic_render_start_date_written
        render_end_date_written = generic_render_end_date_written
        if list_links_to_edit():
            name = tables.LinkColumn(
                "apis:apis_entities:generic_entities_edit_view",
                args=[entity.lower(), A("pk")],
                empty_values=[],
            )
        else:
            name = tables.LinkColumn(
                "apis:apis_entities:generic_entities_detail_view",
                args=[entity.lower(), A("pk")],
                empty_values=[],
            )
        export_formats = [
            "csv",
            "json",
            "xls",
            "xlsx",
        ]
        if "id" in default_cols:
            id = tables.LinkColumn()

        class Meta:
            model = caching.get_ontology_class_of_name(entity)
            fields = default_cols
            attrs = {"class": "table table-hover table-striped table-condensed"}
            # quick ensurance if column is indeed a field of this entity
            for col in default_cols:
                if not hasattr(model, col):
                    raise Exception(
                        f'Model for "{entity}" entity has no field "{col}".\n'
                        f'Check values in "table_fields" list in "entity_settings" '
                        f"(models.py or Settings file)."
                    )

        def __init__(self, *args, **kwargs):
            super().__init__(*args, **kwargs)

    entity_settings = get_entity_settings_by_modelname(entity)
    return entity_settings.get("table", GenericEntitiesTable)
