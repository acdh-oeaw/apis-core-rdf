import warnings
from collections import OrderedDict

import django_tables2 as tables
from apis_core.apis_metainfo.tables import (generic_order_end_date_written,
                                            generic_order_start_date_written,
                                            generic_render_end_date_written,
                                            generic_render_start_date_written)
from apis_core.utils import caching
from django.conf import settings
from django.db.models import Model

from . import MergeColumn


class EntitiesTableFactory:
    """
    Factory class.
    Responsible for creating or retrieving an entity-specific variant of
    the inner GenericEntitiesTable class --> a variant of that class (a class!),
    not an instance of a class.

    The calling code (the calling view) is responsible for creating an
    instance of the returned class and customizing it.

    classmethods:

    get_table_class:
        get already created class or call create_entites_table OR
        if implemented, get a custom class for the specific entity.
    get_custom_table_class:
        hook to retrieve a custom table class listed in settings.
    create_entities_table:
        factory-method responsible for creating a variant of the generic table class
    """

    table_classes = {}

    @classmethod
    def get_custom_table_class(cls, model_name):
        """
        # NOTE: __gp__: unused logic, but for later extensions. Needs proper implementation and documentation. Should then return a class or None.
        Implements a hook to bypass this factory and use a custom table for a specific entity.
        If implemented / used, you MUST use a custom if-branch in apis_entities.views.GenericListViewNew.get_table_kwargs - method!
        Otherwise, the visible_columns costum param will break your implementation.
        Or you can also allow the visible_columns attribute or implement its logic in your custom classes __init__.
        """

        if hasattr(settings, "CUSTOM_ENTITY_TABLES"):
            return settings.CUSTOM_ENTITY_TABLES.get(model_name, None)
        else:
            return None

    @classmethod
    def get_table_class(cls, model_class: Model):
        """
        The entry-point for retrieving a variant of the generic class.
            - if the class does not yet exist, the factory-method 'create_entities_table' is called
                - the factory method creates the class-variant and returns it
                - get_table_class adds this new variant to the lookup-dict 'table_classes'
                - get_table_class returns the new variant
            - if the class was created before, it is fetched from the lookup-dict 'table_classes' and returned directly
        """

        model_name = model_class.__name__
        table_class = cls.table_classes.get(model_name, None)

        if not table_class:

            # this line is the same as saying 'if get_custom_table_class() does not evaluate to False use what custom_table_class returns else use what create_new_entities_table_class() returns'
            table_class = cls.get_custom_table_class(
                model_name
            ) or cls.create_new_entities_table_class(model_class, model_name)
            cls.table_classes[model_name] = table_class
            return table_class

        else:
            return table_class

    @classmethod
    def create_new_entities_table_class(
        cls, model_class: Model, model_name: str
    ):
        class GenericEntitiesTable(tables.Table):
            """
            The Generic Table from which all variants will be cconstructed. Add all possible fields/columns
            as class attributes, if you don't want to use the default fields that django_tables2 chooses 
            based on the model's field's field-type.
            Ideally, implement any custom columns as separate classes and re-use them here. 

            TODO: __gp__: I would suggest a general refactor, that moves all columns, \
            utily functions for tables and columns, their respective Template-snippets \
            and all Factories and Specific tables into a seperate App.
            We duplicated a lot of code across our Apps that could/should be shared / re-used.
            """

            # TODO: __gp__: this should be shared via a GenricBaseTable implementation other tables can inherit from, or via a Mixin.
            # reuse the logic for ordering and rendering *_date_written
            # Important: The names of these class variables must correspond to the column field name,
            # e.g. for start_date_written, the methods must be named order_start_date_written and render_start_date_written
            order_start_date_written = generic_order_start_date_written
            order_end_date_written = generic_order_end_date_written
            render_start_date_written = generic_render_start_date_written
            render_end_date_written = generic_render_end_date_written

            def render_name(self, record, value):
                if value == "":
                    return "(No name provided)"
                else:
                    return value

            export_formats = [
                "csv",
                "json",
                "xls",
                "xlsx",
            ]

            merge = MergeColumn(verbose_name="keep | remove", accessor="pk")
            _detail = tables.TemplateColumn(
                template_name="apis_entities/tables/detail_button_template.html",
                extra_context={"entity_class": model_name},
                verbose_name="",  # __gp__: this ensures the column will have no header
                orderable=False,
                attrs={
                    "td": {"class": "px-0 pl-4 text-center"},
                    "th": {"class": "p-0"},
                },
            )
            _edit = tables.TemplateColumn(
                template_name="apis_entities/tables/edit_button_template.html",
                extra_context={"entity_class": model_name},
                verbose_name="",  # __gp__: this ensures the column will have no header
                orderable=False,
                attrs={
                    "td": {"class": "pl-4 pr-10 text-center"},
                    "th": {"class": "p-0"},
                },
            )

            class Meta:
                """
                __gp__: Please don't use this to customize on a per-entity-basis.
                customization should happen in get_table_kwargs in apis_entities.views.GenericListViewNew.
                Or, if you need access to attributes not available in get_table_kwargs,
                use the __init__ method below.

                F.e. only set exclude here, if you are 100% sure that the fields / columns you
                exclude might NEVER be needed in the future in any case (also for our internal purposes!)
                OR should NEVER be used in ANY table created from this factory.

                This implementation makes use of the default values for the attributes not set in Meta:
                Not setting fields defaults to exposing all fields of the model. No need to add columns
                for those fields, as django_tables2 chooses appropriate columns based on the field-type.

                For further information, see:
                - docs:
                    https://django-tables2.readthedocs.io/en/latest/pages/api-reference.html#table
                - source-code:
                    https://django-tables2.readthedocs.io/en/latest/_modules/django_tables2/tables.html#Table
                """

                model = model_class
                attrs = {
                    "class": "table table-hover table-striped table-condensed"
                }

            def __init__(
                self, visible_columns: tuple[str] = None, *args, **kwargs
            ):
                """
                Extends how table instances are instanciated.
                Adds the visible_columns param (not provided by django_tables2),
                which must be an iterable of column-names.
                Only the columns given in visible_columns will be added to the table.
                If visible_columns is not set, a warning will be raised (not an error).

                TODO: Currently, exporting table data as csv, etc. is disabled.
                TODO: If re-implemented, ensure that visible_columns also applies to the exported table data.
                """
                super().__init__(*args, **kwargs)

                if not visible_columns:
                    warnings.warn(
                        ">>>>>>>> WARNING! You SHOULD set the param 'visible_columns', or the user will see all columns available for the model! <<<<<<<<"
                    )
                else:
                    for col_name in self.base_columns:
                        if col_name not in visible_columns:
                            self.columns.hide(col_name)

        return GenericEntitiesTable
