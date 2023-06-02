import django_tables2 as tables
from apis_core.apis_metainfo.tables import (
    generic_order_start_date_written,
    generic_order_end_date_written,
    generic_render_start_date_written,
    generic_render_end_date_written,
)
from apis_core.utils import caching
from . import MergeColumn

class EntitiesTableFactory:
    """
    Factory class that is responsible for creating or retrieving an entity-specific 
    variant of the GenericEntiesTable-class (a variant of that class (a class!), not an instance of a class).

    The calling code (the calling view) is responsible for creating an instance of the returned class.

    methods: 

    get_table_class:
      - is the entry-point for retrieving a variant of the generic class. 
      - if the class does not yet exist, the factory-method 'create_entities_table' is called
        - the factory method creates the class-variant and returns it
        - get_table_class adds this new variant to the lookup-dict 'table_classes'
        - get_table_class returns the new variant
      - if the class was created before, it is fetched from the lookup-dict 'table_classes' and returned directly

    create_entities_table:
        factory-method responsible for creating a variant of the generic table class
    """
    table_classes = {}

    def render_name(self, record, value):
        if value == "":
            return "(No name provided)"
        else:
            return value

    @classmethod
    def get_table_class(cls, entity_name:str):
        table_class = cls.table_classes.get(entity_name, None)

        if not table_class:
            table_class = cls.create_new_entities_table_class(entity_name)
            cls.table_classes[entity_name] = table_class
            return table_class
        
        else: 
            return table_class
        
    @classmethod
    def create_new_entities_table_class(cls, entity_name:str):
        if default_cols is None:
            default_cols = [
                "name",
            ]

        class GenericEntitiesTable(tables.Table):
           

            # reuse the logic for ordering and rendering *_date_written
            # Important: The names of these class variables must correspond to the column field name,
            # e.g. for start_date_written, the methods must be named order_start_date_written and render_start_date_written
            order_start_date_written = generic_order_start_date_written
            order_end_date_written = generic_order_end_date_written
            render_start_date_written = generic_render_start_date_written
            render_end_date_written = generic_render_end_date_written
            # if edit_v:
            #     name = tables.LinkColumn(
            #         "apis:apis_entities:generic_entities_edit_view",
            #         args=[entity.lower(), A("pk")],
            #         empty_values=[],
            #     )
            # else:
            #     name = tables.LinkColumn(
            #         "apis:apis_entities:generic_entities_detail_view",
            #         args=[entity.lower(), A("pk")],
            #         empty_values=[],
            #     )
            export_formats = [
                "csv",
                "json",
                "xls",
                "xlsx",
            ]
            #if "merge" in default_cols:
            merge = MergeColumn(verbose_name="keep | remove", accessor="pk")
            #if "id" in default_cols:
            #    id = tables.LinkColumn()

            class Meta:
                model = caching.get_ontology_class_of_name(entity_name)
                exclude = ['pk'] # GP: intended use: only add fields here to exclude that should NEVER be used, in any foreseeable case, by any instance of the table class!
                attrs = {"class": "table table-hover table-striped table-condensed"}
        
            def __init__(self, include_detail_and_edit:bool=True, *args, **kwargs):

                if include_detail_and_edit:
                    self.
                super().__init__(*args, **kwargs)

        return GenericEntitiesTable





# def get_entities_table(entity, edit_v, default_cols):
#     if default_cols is None:
#         default_cols = [
#             "name",
#         ]

#     class GenericEntitiesTable(tables.Table):
#         def render_name(self, record, value):
#             if value == "":
#                 return "(No name provided)"
#             else:
#                 return value

#         # reuse the logic for ordering and rendering *_date_written
#         # Important: The names of these class variables must correspond to the column field name,
#         # e.g. for start_date_written, the methods must be named order_start_date_written and render_start_date_written
#         order_start_date_written = generic_order_start_date_written
#         order_end_date_written = generic_order_end_date_written
#         render_start_date_written = generic_render_start_date_written
#         render_end_date_written = generic_render_end_date_written
#         if edit_v:
#             name = tables.LinkColumn(
#                 "apis:apis_entities:generic_entities_edit_view",
#                 args=[entity.lower(), A("pk")],
#                 empty_values=[],
#             )
#         else:
#             name = tables.LinkColumn(
#                 "apis:apis_entities:generic_entities_detail_view",
#                 args=[entity.lower(), A("pk")],
#                 empty_values=[],
#             )
#         export_formats = [
#             "csv",
#             "json",
#             "xls",
#             "xlsx",
#         ]
#         if "merge" in default_cols:
#             merge = MergeColumn(verbose_name="keep | remove", accessor="pk")
#         if "id" in default_cols:
#             id = tables.LinkColumn()

#         class Meta:
#             model = caching.get_ontology_class_of_name(entity)
#             fields = default_cols
#             attrs = {"class": "table table-hover table-striped table-condensed"}
#             # quick ensurance if column is indeed a field of this entity
#             for col in default_cols:
#                 if not hasattr(model, col):
#                     raise Exception(
#                         f'Model for "{entity}" entity has no field "{col}".\n'
#                         f'Check values in "table_fields" list in "entity_settings" '
#                         f"(models.py or Settings file)."
#                     )

#         def __init__(self, *args, **kwargs):
#             super().__init__(*args, **kwargs)

#     return GenericEntitiesTable
