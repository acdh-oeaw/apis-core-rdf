import django_tables2 as tables
from django.conf import settings
from django.db.models import Case, When, F, Q
from django.template.loader import render_to_string
from django.utils.html import format_html
from django_tables2.utils import A
from apis_core.apis_entities.models import AbstractEntity
from apis_core.apis_labels.models import Label
from apis_core.apis_metainfo.models import Uri
from apis_core.apis_metainfo.tables import (
    generic_order_start_date_written,
    generic_order_end_date_written,
    generic_render_start_date_written,
    generic_render_end_date_written,
)
from apis_core.apis_relations.models import Triple, Property
from apis_core.helper_functions import caching

empty_text_default = "There are currently no relations"

def render_triple_table(
    model_self_class_str,
    model_other_class_str,
    model_self_id_str,
    should_be_editable,
    request,
):
    """
    renders the table of properties and entities of related triples. To be used for a quick
    overview in an entity detail or edit view. Also, if needed with ajax calls prepared and
    integrated into the rows for edit and delete purpose.
    
    :param model_self_class_str: str representation of the main entity class, always referred as
    self, in django's lowercase format
    :param model_other_class_str: str representation of the other entity class, always referred as
    self, in django's lowercase format
    :param model_self_id_str: the id of the main entity instance, needed for creating triples
    :param should_be_editable: toggle if this should be rendered with edit buttons or not (for
    entity detail and edit view separately)
    :param request: the request object, needed for the table for whatever reason. Could not leave
    it out.
    :return: a html rendered string to be integrated into the calling view
    """
    
    class TripleTable(tables.Table):
        # Since the main entity can be either subject or object of a triple, we need 'other' fields
        other_prop = tables.Column(empty_values=())
        other_entity = tables.Column(empty_values=())
        if should_be_editable:
            edit = tables.Column(empty_values=())
            delete = tables.Column(empty_values=())
        
        class Meta:
            model = Triple
            fields = ["other_prop", "other_entity"]
            if should_be_editable:
                fields += ["edit", "delete"]
                if "apis_bibsonomy" in settings.INSTALLED_APPS:
                    fields = ["ref"] + fields
            # If I would use `template_name` here, django-tables crashes. Perhaps it only expects some
            # of its own pre-integrated templates? But since I want to use a custom one and also attach it
            # to this class I renamed it to `template_name_custom`. I did not find a better solution quickly.
            template_name_custom = "apis_relations/triple_table.html"
    
        def __init__(self, *args, **kwargs):
            model_self_class = caching.get_ontology_class_of_name(model_self_class_str)
            model_self_instance = model_self_class.objects.get(pk=model_self_id_str)
            model_other_class = caching.get_ontology_class_of_name(model_other_class_str)
            model_other_contenttype = caching.get_contenttype_of_class(model_other_class)
            # get the data that is only related to current main entity
            data = Triple.objects.filter(
                (
                    Q(subj=model_self_instance)
                    & Q(obj__self_content_type=model_other_contenttype)
                )
                | (
                    Q(obj=model_self_instance)
                    & Q(subj__self_content_type=model_other_contenttype)
                )
            ).distinct()
            self.base_columns["other_prop"].verbose_name = "Other property"
            self.base_columns["other_entity"].verbose_name = \
                f"Related {model_other_class.__name__.title()}"
            if "apis_bibsonomy" in settings.INSTALLED_APPS:
                self.base_columns["ref"] = tables.TemplateColumn(
                    template_name="apis_relations/references_button_generic_ajax_form.html"
                )
            super().__init__(data, *args, **kwargs)

        def render_other_prop(self, record):
            """
            displays the correct name direction of the related property with respect to main entity
    
            :param record: the current triple instance
            :return: related property name
            """
    
            # TODO: Make the related properties clickable (like it was in vanilla).
            if str(record.subj.pk) == model_self_id_str:
                return record.prop.name
            elif str(record.obj.pk) == model_self_id_str:
                return record.prop.name_reverse
            else:
                raise Exception(
                    "Did not find the entity this relation is supposed to come from!"
                    + "Something must have went wrong when annotating for the related instance."
                )

        def render_other_entity(self, record):
            """
            displays the other entity for each row
    
            :param record: the current triple instance
            :return: related instance
            """

            # TODO: Make the related entities clickable (like it was in vanilla).
            if str(record.subj.pk) == model_self_id_str:
                return record.obj
            elif str(record.obj.pk) == model_self_id_str:
                return record.subj
            else:
                raise Exception(
                    "Did not find the entity this relation is supposed to come from!"
                    + "Something must have went wrong when annotating for the related instance."
                )
            
        def render_edit(self, record):
            """
            renders the html for the button and injects the record pk into ajax call
            
            :param record: triple instance
            :return: rendered html button
            """
            
            return format_html(f"""
                    <a class='reledit' onclick="ajax_2_load_triple_form(div_origin=this, triple_id={record.pk})">
                    <svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" class="feather feather-edit-2">
                        <polygon points="16 3 21 8 8 21 3 21 3 16 16 3"></polygon>
                    </svg>
                </a>
            """)

        def render_delete(self, record):
            """
            renders the html for the button and injects the record pk into ajax call
            
            :param record: triple instance
            :return: rendered html button
            """
            
            return format_html(f"""
                <a class='reledit' onclick="ajax_2_delete_triple(div_origin=this, triple_id={record.id})">
                    <svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" class="feather feather-trash">
                        <polyline points="3 6 5 6 21 6">
                        </polyline>
                        <path d="M19 6v14a2 2 0 0 1-2 2H7a2 2 0 0 1-2-2V6m3 0V4a2 2 0 0 1 2-2h4a2 2 0 0 1 2 2v2">
                        </path>
                    </svg>
                </a>
            """)
        
    return render_to_string(
        request=request,
        template_name=TripleTable.Meta.template_name_custom,
        context={"table": TripleTable()},
    )

def render_reification_table(
    model_self_class_str,
    reification_type_str,
    model_self_id_str,
    should_be_editable,
    request,
):
    """
    renders the table of related reifications plus their related entities. To be used for a quick
    overview in an entity detail or edit view. Also, if needed with ajax calls prepared and
    integrated into the rows for edit and delete purpose.
    
    :param model_self_class_str: str representation of the main entity class, always referred as
    self, in django's lowercase format
    :param reification_type_str: str representation of the reification class, always referred as
    self, in django's lowercase format
    :param model_self_id_str: the id of the main entity instance, needed for creating triples
    :param should_be_editable: toggle if this should be rendered with edit buttons or not (for
    entity detail and edit view separately)
    :param request: the request object, needed for the table for whatever reason. Could not leave
    it out.
    :return: a html rendered string to be integrated into the calling view
    """
    
    reification_class = caching.get_reification_class_of_name(reification_type_str)
    model_self_class = caching.get_entity_class_of_name(model_self_class_str)
    model_self_instance = model_self_class.objects.get(pk=model_self_id_str)

    class ReificationTable(tables.Table):
        related_entities = tables.Column(empty_values=())
        if should_be_editable:
            # It needs empty_values=(), otherwise the button icons would only render on the second
            # call. No idea why.
            edit = tables.Column(empty_values=())
            delete = tables.Column(empty_values=())
        
        class Meta:
            model = reification_class
            fields = ["name", "related_entities"]
            if should_be_editable:
                fields += ["edit", "delete"]
            # If I would use `template_name` here, django-tables crashes. Perhaps it only expects
            # some of its own pre-integrated templates? But since we want to use a custom one and
            # also attach it to this class I renamed it to `template_name_custom`. I did not find a
            # better solution quickly.
            template_name_custom = "apis_relations/reification_table.html"
        
        def __init__(self, *args, **kwargs):
            super().__init__(
                *args,
                **kwargs,
                data=reification_class.objects.filter(
                    Q(triple_set_from_obj__subj=model_self_instance)
                    | Q(triple_set_from_obj__subj=model_self_instance)
                ).distinct()
            )
            
        def render_related_entities(self, record):
            """
            this method iterates over all entities that are:
            1. related to the reification of the current row
            2. are not the entity self which is the main entity we are viewing
            
            :param record: the reification instance, passed by the django-tables' logic
            :return: a html string containing all related entities to be displayed in a row
            """
            
            # TODO: Make the related entities clickable (like it was in vanilla).
            # note that this would also require a differentiation between detail and edit linking
            related_other_entities = []
            for triple in Triple.objects.filter(Q(subj=record) | Q(obj=record)):
                if triple.subj != record and triple.subj != model_self_instance:
                    related_other_entities.append(triple.subj)
                elif triple.obj != record and triple.obj != model_self_instance:
                    related_other_entities.append(triple.obj)
            related_other_entities = ", ".join([e.name for e in related_other_entities])
            return format_html(f"{related_other_entities}")
        
        def render_edit(self, record):
            """
            This renders a button that calls ajax logic to load the record reification into a form.
            
            Usually it's cleaner to avoid html code here in the python module and keep it with other
            templates, but rendering it here has the advantage of having access to the reification
            as full python object. Right now we only use its id, but should we need more elaborate
            logic the record python object here would come in handy.
            
            :param record: the reification instance, passed by the django-tables' logic
            :return: a html button
            """
            
            return format_html(f"""
                    <a class='reledit' onclick="ajax_2_load_reification_form(div_origin=this, reification_id={record.id})">
                    <svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" class="feather feather-edit-2">
                        <polygon points="16 3 21 8 8 21 3 21 3 16 16 3"></polygon>
                    </svg>
                </a>
            """)

        def render_delete(self, record):
            """
            This renders a button that calls ajax logic to delete the record reification.
            
            Usually it's cleaner to avoid html code here in the python module and keep it with other
            templates, but rendering it here has the advantage of having access to the reification
            as full python object. Right now we only use its id, but should we need more elaborate
            logic the record python object here would come in handy.
            
            :param record: the reification instance, passed by the django-tables' logic
            :return: a html button
            """
            return format_html(f"""
                <a class='reledit' onclick="ajax_2_delete_reification(div_origin=this, reification_id={record.id})">
                    <svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" class="feather feather-trash">
                        <polyline points="3 6 5 6 21 6">
                        </polyline>
                        <path d="M19 6v14a2 2 0 0 1-2 2H7a2 2 0 0 1-2-2V6m3 0V4a2 2 0 0 1 2-2h4a2 2 0 0 1 2 2v2">
                        </path>
                    </svg>
                </a>
            """)

    return render_to_string(
        request=request,
        template_name=ReificationTable.Meta.template_name_custom,
        context={"table": ReificationTable()},
    )


# TODO RDF : combine this or re-use this class here in get_generic_triple_table
# TODO RDF : Also consider implementing proper form search fields for this (instead of default drop-downs)
class TripleTable_OLD(tables.Table):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    class Meta:
        model = Triple
        fields = [
            "id",
            "subj",
            "prop",
            "obj",
        ]
        sequence = tuple(fields)
        attrs = {"class": "table table-hover table-striped table-condensed"}


class PropertyTable(tables.Table):
    """Construct table for properties.

    The table shows how entities connect with one another via properties (relations).
    It uses the format of an RDF triple – Subject-Predicate-Object – plus
    "Reverse Predicate" for the inverse relationship and is displayed on the frontend
     on the Relations > Property page.
    """

    # Note on constructing table columns / usage of variables:
    # The variables used to declare table columns need to have the same names
    # as the model field names from which the columns should be created,
    # or tables.Column needs to contain an attribute "accessor" which references
    # the original field name.
    # For columns which allow sorting, the variable names are used as sort strings
    # in the user's browser address bar, so for UX reasons, it may make sense to
    # use different variable names than the original field names.

    predicate = tables.Column(
        accessor="name_forward",  # original field name in model class
        verbose_name="Predicate",
    )
    predicate_reverse = tables.Column(
        accessor="name_reverse",  # original field name in model class
        verbose_name="Reverse predicate",
    )

    subject = tables.ManyToManyColumn(
        accessor="subj_class",  # original field name in model class
        verbose_name="Subject",
        separator=format_html(",<br>"),
        orderable=True,
        filter=lambda qs: qs.order_by(
            "model"
        ),  # order retrieved objects within table cell
        # use .name for model verbose name, .model for model class name
        transform=lambda ent: f"{ent.model.title()}",
        linkify_item={
            "viewname": "apis_core:apis_entities:generic_entities_list",
            "args": [tables.A("model")],
        },
    )

    object = tables.ManyToManyColumn(
        accessor="obj_class",  # original field name in model class
        verbose_name="Object",
        separator=format_html(",<br>"),
        orderable=True,
        filter=lambda qs: qs.order_by(
            "model"
        ),  # order retrieved objects within table cell
        # use .name for model verbose name, .model for model class name
        transform=lambda ent: f"{ent.model.title()}",
        linkify_item={
            "viewname": "apis_core:apis_entities:generic_entities_list",
            "args": [tables.A("model")],
        },
    )

    class Meta:
        model = Property
        fields = []
        sequence = [
            "subject",
            "predicate",
            "object",
            "predicate_reverse",
        ]
        order_by = "predicate"
        attrs = {"class": "table table-hover table-striped table-condensed"}

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    # Use order_ methods to define how individual columns should be sorted.
    # Method names are column names prefixed with "order_".
    # By default, columns for regular fields are sorted alphabetically; for
    # ManyToMany fields, however, the row IDs of the originating table are
    # used as basis for sorting.
    # When column names and field names differ (see earlier note), the original
    # field names need to be referenced when constructing queryset.
    def order_subject(self, queryset, is_descending):
        queryset = queryset.annotate(entity=F("subj_class__model")).order_by(
            ("-" if is_descending else "") + "entity"
        )
        return (queryset, True)

    def order_object(self, queryset, is_descending):
        queryset = queryset.annotate(entity=F("obj_class__model")).order_by(
            ("-" if is_descending else "") + "entity"
        )
        return (queryset, True)


def get_generic_relation_listview_table(relation_name):
    """
    Creates a table class according to the relation class given by the relation_name parameter.
    Instantiates corresponding columns which also provide linking to the respectively related entities.

    :param relation_name: str : The name of the relation class to be loaded
    :return: a django-tables2 Table Class tailored for the respective relation class
    """

    # create all variables which save the foreign key fields which are different for each relation class
    relation_class = AbstractRelation.get_relation_class_of_name(relation_name)
    related_entity_class_name_a = (
        relation_class.get_related_entity_classA().__name__.lower()
    )
    related_entity_class_name_b = (
        relation_class.get_related_entity_classB().__name__.lower()
    )
    related_entity_field_name_a = relation_class.get_related_entity_field_nameA()
    related_entity_field_name_b = relation_class.get_related_entity_field_nameB()

    class GenericRelationListViewTable(tables.Table):

        # reuse the logic for ordering and rendering *_date_written
        # Important: The names of these class variables must correspond to the column field name,
        # e.g. for start_date_written, the methods must be named order_start_date_written and render_start_date_written
        order_start_date_written = generic_order_start_date_written
        order_end_date_written = generic_order_end_date_written
        render_start_date_written = generic_render_start_date_written
        render_end_date_written = generic_render_end_date_written

        class Meta:
            model = relation_class

            # the fields list also serves as the defining order of them, as to avoid duplicated definitions
            fields = [
                related_entity_field_name_a,
                related_entity_field_name_b,
                "relation_type",
                "start_date_written",
                "end_date_written",
            ]
            # reuse the list for ordering
            sequence = tuple(fields)

            # This attrs dictionary I took over from the tables implementation before. No idea if and where it would be needed.
            attrs = {"class": "table table-hover table-striped table-condensed"}

        def __init__(self, *args, **kwargs):

            # LinkColumn objects provied hyperlinking to the related entities
            self.base_columns[related_entity_field_name_a] = tables.LinkColumn(
                # which url to use:
                "apis:apis_entities:generic_entities_detail_view",
                args=[
                    # which entity sub-url to load from:
                    related_entity_class_name_a,
                    # which instance identifier to use:
                    A(related_entity_field_name_a + ".pk"),
                ],
            )

            # same as above
            self.base_columns[related_entity_field_name_b] = tables.LinkColumn(
                "apis:apis_entities:generic_entities_detail_view",
                args=[
                    related_entity_class_name_b,
                    A(related_entity_field_name_b + ".pk"),
                ],
            )

            super().__init__(*args, **kwargs)

    return GenericRelationListViewTable


def get_generic_relations_table(relation_class, entity_instance, detail=None):
    """
    Creates a table class according to the relation and entity class given by the parameters.

    :param relation_class: the class where the entity_instance can have instantiated relations to
    :param entity_instance: the entity instance of which related relations and entities are to be displayed
    :param detail: boolean : if this Table is to be displayed in an detail or edit UI
    :return: a django-tables2 Table Class tailored for the respective relation class and entity instance
    """

    # create all variables which save the foreign key fields which are different for each relation class
    entity_class_name = entity_instance.__class__.__name__.lower()
    related_entity_class_name_a = (
        relation_class.get_related_entity_classA().__name__.lower()
    )
    related_entity_class_name_b = (
        relation_class.get_related_entity_classB().__name__.lower()
    )
    related_entity_field_name_a = relation_class.get_related_entity_field_nameA()
    related_entity_field_name_b = relation_class.get_related_entity_field_nameB()

    # find out what other entity class the current entity instance in a given relation class is related to
    # (needed for linkg towards instances of related entities)
    if entity_class_name == related_entity_class_name_a == related_entity_class_name_b:
        other_related_entity_class_name = entity_class_name

    elif entity_class_name == related_entity_class_name_a:
        other_related_entity_class_name = related_entity_class_name_b

    elif entity_class_name == related_entity_class_name_b:
        other_related_entity_class_name = related_entity_class_name_a

    else:
        raise Exception(
            "Did not find the entity instance in the given relation class fields!"
            + "Either a wrong entity instance or wrong relation class was passed to this function."
        )

    class RelationTableBase(tables.Table):
        """
        The base table from which detail or edit tables will inherit from in order to avoid redundant definitions
        """

        # reuse the logic for ordering and rendering *_date_written
        # Important: The names of these class variables must correspond to the column field name,
        # e.g. for start_date_written, the methods must be named order_start_date_written and render_start_date_written
        order_start_date_written = generic_order_start_date_written
        order_end_date_written = generic_order_end_date_written
        render_start_date_written = generic_render_start_date_written
        render_end_date_written = generic_render_end_date_written

        class Meta:
            """
            Meta class needed for django-tables2 plugin.
            """

            empty_text = empty_text_default
            model = relation_class

            # the fields list also serves as the defining order of them, as to avoid duplicated definitions
            fields = [
                "start_date_written",
                "end_date_written",
                "other_relation_type",
                "other_related_entity",
            ]
            # reuse the list for ordering
            sequence = tuple(fields)

            # This attrs dictionary I took over from the tables implementation before. No idea if and where it would be needed.
            attrs = {
                "class": "table table-hover table-striped table-condensed",
                "id": related_entity_class_name_a.title()[:2]
                + related_entity_class_name_b.title()[:2]
                + "_conn",
            }

        def render_other_related_entity(self, record, value):
            """
            Custom render_FOO method for related entity linking. Since the 'other_related_entity' is a generated annotation
            on the queryset, it does not return the related instance but only the foreign key as the integer it is.
            Thus fetching the related instance is necessary.

            :param record: The 'row' of a queryset, i.e. an entity instance
            :param value: The current column of the row, i.e. the 'other_related_entity' annotation
            :return: related instance
            """

            if value == record.get_related_entity_instanceA().pk:
                return record.get_related_entity_instanceA()

            elif value == record.get_related_entity_instanceB().pk:
                return record.get_related_entity_instanceB()

            else:
                raise Exception(
                    "Did not find the entity this relation is supposed to come from!"
                    + "Something must have went wrong when annotating for the related instance."
                )

        def __init__(self, data, *args, **kwargs):

            # annotations for displaying data about the 'other side' of the relation.
            # Both of them ('other_related_entity' and 'other_relation_type') are necessary for displaying relations
            # in context to what entity we are calling this from.
            data = data.annotate(
                # In order to provide the 'other instance' for each instance of a table where this whole logic is called from,
                # the queryset must be annotated accordingly. The following Case searches which of the two related instances
                # of a relation queryset entry is the one corresponding to the current entity instance. When found, take the
                # other related entity (since this is the one we are interested in displaying).
                #
                # The approach of using queryset's annotate method allows for per-instance case decision and thus
                # guarantees that the other related entity is always correctly picked,
                # even in case two entities are of the same class.
                other_related_entity=Case(
                    # **kwargs pattern is needed here as the key-value pairs change with each relation class and entity instance.
                    When(
                        **{
                            related_entity_field_name_a + "__pk": entity_instance.pk,
                            "then": related_entity_field_name_b,
                        }
                    ),
                    When(
                        **{
                            related_entity_field_name_b + "__pk": entity_instance.pk,
                            "then": related_entity_field_name_a,
                        }
                    ),
                )
            ).annotate(
                # Get the correct side of the relation type given the current entity instance.
                #
                # The approach of using queryset's annotate method allows for per-instance case decision and thus
                # guarantees that the other related entity is always correctly picked,
                # even in case two entities are of the same class.
                other_relation_type=Case(
                    When(
                        **{
                            # A->B relation and current entity instance is A, hence take forward name
                            related_entity_field_name_a + "__pk": entity_instance.pk,
                            "then": "relation_type__name",
                        }
                    ),
                    When(
                        **{
                            # A->B relation and current entity instance is B, hence take reverse name.
                            related_entity_field_name_b + "__pk": entity_instance.pk,
                            "then": "relation_type__name_reverse",
                        }
                    ),
                )
            )
            for an in data:
                if (
                    getattr(an, f"{related_entity_field_name_a}_id")
                    == entity_instance.pk
                ):
                    an.other_relation_type = getattr(an.relation_type, "label")
                else:
                    an.other_relation_type = getattr(an.relation_type, "label_reverse")

            super().__init__(data, *args, **kwargs)

    if detail:

        class RelationTableDetail(RelationTableBase):
            """
            Sublcass inheriting the bulk of logic from parent. This table is used for the 'detail' views.
            """

            def __init__(self, data, *args, **kwargs):

                # Only addition with respect to parent class is which main url is to be used when clicking on a
                # related entity column.
                self.base_columns["other_related_entity"] = tables.LinkColumn(
                    "apis:apis_entities:generic_entities_detail_view",
                    args=[other_related_entity_class_name, A("other_related_entity")],
                    verbose_name="Related " + other_related_entity_class_name.title(),
                )

                super().__init__(data=data, *args, **kwargs)

        return RelationTableDetail

    else:

        class RelationTableEdit(RelationTableBase):
            """
            Sublcass inheriting the bulk of logic from parent. This table is used for the 'edit' view.
            """

            class Meta(RelationTableBase.Meta):
                """
                Additional Meta fields are necessary for editing functionalities
                """

                # This fields list also defines the order of the elements.
                fields = ["delete"] + RelationTableBase.Meta.fields + ["edit"]

                if "apis_bibsonomy" in settings.INSTALLED_APPS:
                    fields = ["ref"] + fields

                # again reuse the fields list for ordering
                sequence = tuple(fields)

            def __init__(self, *args, **kwargs):

                # Clicking on a related entity will lead also the edit view of the related entity instance
                self.base_columns["other_related_entity"] = tables.LinkColumn(
                    "apis:apis_entities:generic_entities_edit_view",
                    args=[other_related_entity_class_name, A("other_related_entity")],
                    verbose_name="Related " + other_related_entity_class_name.title(),
                )

                # delete button
                self.base_columns["delete"] = tables.TemplateColumn(
                    template_name="apis_relations/delete_button_generic_ajax_form.html"
                )

                # edit button
                self.base_columns["edit"] = tables.TemplateColumn(
                    template_name="apis_relations/edit_button_generic_ajax_form.html"
                )

                # bibsonomy button
                if "apis_bibsonomy" in settings.INSTALLED_APPS:
                    self.base_columns["ref"] = tables.TemplateColumn(
                        template_name="apis_relations/references_button_generic_ajax_form.html"
                    )

                super().__init__(*args, **kwargs)

        return RelationTableEdit


# __before_rdf_refactoring__
#
# def get_generic_relations_table(relation_class, entity_instance, detail=None):
#     """
#     Creates a table class according to the relation and entity class given by the parameters.
#
#     :param relation_class: the class where the entity_instance can have instantiated relations to
#     :param entity_instance: the entity instance of which related relations and entities are to be displayed
#     :param detail: boolean : if this Table is to be displayed in an detail or edit UI
#     :return: a django-tables2 Table Class tailored for the respective relation class and entity instance
#     """
#
#     # create all variables which save the foreign key fields which are different for each relation class
#     entity_class_name = entity_instance.__class__.__name__.lower()
#     related_entity_class_name_a = relation_class.get_related_entity_classA().__name__.lower()
#     related_entity_class_name_b = relation_class.get_related_entity_classB().__name__.lower()
#     related_entity_field_name_a = relation_class.get_related_entity_field_nameA()
#     related_entity_field_name_b = relation_class.get_related_entity_field_nameB()
#
#     # find out what other entity class the current entity instance in a given relation class is related to
#     # (needed for linkg towards instances of related entities)
#     if entity_class_name == related_entity_class_name_a == related_entity_class_name_b:
#         other_related_entity_class_name = entity_class_name
#
#     elif entity_class_name == related_entity_class_name_a:
#         other_related_entity_class_name = related_entity_class_name_b
#
#     elif entity_class_name == related_entity_class_name_b:
#         other_related_entity_class_name = related_entity_class_name_a
#
#     else:
#         raise Exception(
#             "Did not find the entity instance in the given relation class fields!" +
#             "Either a wrong entity instance or wrong relation class was passed to this function."
#         )
#
#
#     class RelationTableBase(tables.Table):
#         """
#         The base table from which detail or edit tables will inherit from in order to avoid redundant definitions
#         """
#
#         # reuse the logic for ordering and rendering *_date_written
#         # Important: The names of these class variables must correspond to the column field name,
#         # e.g. for start_date_written, the methods must be named order_start_date_written and render_start_date_written
#         order_start_date_written = generic_order_start_date_written
#         order_end_date_written = generic_order_end_date_written
#         render_start_date_written = generic_render_start_date_written
#         render_end_date_written = generic_render_end_date_written
#
#         class Meta:
#             """
#             Meta class needed for django-tables2 plugin.
#             """
#
#             empty_text = empty_text_default
#             model = relation_class
#
#             # the fields list also serves as the defining order of them, as to avoid duplicated definitions
#             fields = [
#                 'start_date_written',
#                 'end_date_written',
#                 'other_relation_type',
#                 "other_related_entity"
#             ]
#             # reuse the list for ordering
#             sequence = tuple(fields)
#
#             # This attrs dictionary I took over from the tables implementation before. No idea if and where it would be needed.
#             attrs = {
#                 "class": "table table-hover table-striped table-condensed",
#                 "id": related_entity_class_name_a.title()[:2] + related_entity_class_name_b.title()[:2] + "_conn"
#             }
#
#         def render_other_related_entity(self, record, value):
#             """
#             Custom render_FOO method for related entity linking. Since the 'other_related_entity' is a generated annotation
#             on the queryset, it does not return the related instance but only the foreign key as the integer it is.
#             Thus fetching the related instance is necessary.
#
#             :param record: The 'row' of a queryset, i.e. an entity instance
#             :param value: The current column of the row, i.e. the 'other_related_entity' annotation
#             :return: related instance
#             """
#
#             if value == record.get_related_entity_instanceA().pk :
#                 return record.get_related_entity_instanceA()
#
#             elif value == record.get_related_entity_instanceB().pk :
#                 return record.get_related_entity_instanceB()
#
#             else:
#                 raise Exception(
#                     "Did not find the entity this relation is supposed to come from!" +
#                     "Something must have went wrong when annotating for the related instance."
#                 )
#
#
#         def __init__(self, data, *args, **kwargs):
#
#             # annotations for displaying data about the 'other side' of the relation.
#             # Both of them ('other_related_entity' and 'other_relation_type') are necessary for displaying relations
#             # in context to what entity we are calling this from.
#             data = data.annotate(
#                 # In order to provide the 'other instance' for each instance of a table where this whole logic is called from,
#                 # the queryset must be annotated accordingly. The following Case searches which of the two related instances
#                 # of a relation queryset entry is the one corresponding to the current entity instance. When found, take the
#                 # other related entity (since this is the one we are interested in displaying).
#                 #
#                 # The approach of using queryset's annotate method allows for per-instance case decision and thus
#                 # guarantees that the other related entity is always correctly picked,
#                 # even in case two entities are of the same class.
#                 other_related_entity=Case(
#                     # **kwargs pattern is needed here as the key-value pairs change with each relation class and entity instance.
#                     When(**{
#                         related_entity_field_name_a + "__pk": entity_instance.pk,
#                         "then": related_entity_field_name_b
#                     }),
#                     When(**{
#                         related_entity_field_name_b + "__pk": entity_instance.pk,
#                         "then": related_entity_field_name_a
#                     }),
#                 )
#             ).annotate(
#                 # Get the correct side of the relation type given the current entity instance.
#                 #
#                 # The approach of using queryset's annotate method allows for per-instance case decision and thus
#                 # guarantees that the other related entity is always correctly picked,
#                 # even in case two entities are of the same class.
#                 other_relation_type=Case(
#                     When(**{
#                         # A->B relation and current entity instance is A, hence take forward name
#                         related_entity_field_name_a + "__pk": entity_instance.pk,
#                         "then": "relation_type__name"
#                     }),
#                     When(**{
#                         # A->B relation and current entity instance is B, hence take reverse name.
#                         related_entity_field_name_b + "__pk": entity_instance.pk,
#                         "then": "relation_type__name_reverse"
#                     }),
#                 )
#             )
#             for an in data:
#                 if getattr(an, f"{related_entity_field_name_a}_id") == entity_instance.pk:
#                     an.other_relation_type = getattr(an.relation_type, "label")
#                 else:
#                     an.other_relation_type = getattr(an.relation_type, "label_reverse")
#
#
#             super().__init__(data, *args, **kwargs)
#
#
#     if detail:
#
#         class RelationTableDetail(RelationTableBase):
#             """
#             Sublcass inheriting the bulk of logic from parent. This table is used for the 'detail' views.
#             """
#
#             def __init__(self, data, *args, **kwargs):
#
#                 # Only addition with respect to parent class is which main url is to be used when clicking on a
#                 # related entity column.
#                 self.base_columns["other_related_entity"] = tables.LinkColumn(
#                     'apis:apis_entities:generic_entities_detail_view',
#                     args=[
#                         other_related_entity_class_name,
#                         A("other_related_entity")
#                     ],
#                     verbose_name="Related " + other_related_entity_class_name.title()
#                 )
#
#                 super().__init__(data=data, *args, **kwargs)
#
#
#         return RelationTableDetail
#
#
#     else:
#
#         class RelationTableEdit(RelationTableBase):
#             """
#             Sublcass inheriting the bulk of logic from parent. This table is used for the 'edit' view.
#             """
#
#             class Meta(RelationTableBase.Meta):
#                 """
#                 Additional Meta fields are necessary for editing functionalities
#                 """
#
#                 # This fields list also defines the order of the elements.
#                 fields = ["delete"] + RelationTableBase.Meta.fields + ["edit"]
#
#                 if 'apis_bibsonomy' in settings.INSTALLED_APPS:
#                     fields = ["ref"] + fields
#
#                 # again reuse the fields list for ordering
#                 sequence = tuple(fields)
#
#
#             def __init__(self, *args, **kwargs):
#
#                 # Clicking on a related entity will lead also the edit view of the related entity instance
#                 self.base_columns["other_related_entity"] = tables.LinkColumn(
#                     'apis:apis_entities:generic_entities_edit_view',
#                     args=[
#                         other_related_entity_class_name, A("other_related_entity")
#                     ],
#                     verbose_name="Related " + other_related_entity_class_name.title()
#                 )
#
#                 # delete button
#                 self.base_columns['delete'] = tables.TemplateColumn(
#                     template_name='apis_relations/delete_button_generic_ajax_form.html'
#                 )
#
#                 # edit button
#                 self.base_columns['edit'] = tables.TemplateColumn(
#                     template_name='apis_relations/edit_button_generic_ajax_form.html'
#                 )
#
#                 # bibsonomy button
#                 if 'apis_bibsonomy' in settings.INSTALLED_APPS:
#                     self.base_columns['ref'] = tables.TemplateColumn(
#                         template_name='apis_relations/references_button_generic_ajax_form.html'
#                     )
#
#                 super().__init__(*args, **kwargs)
#
#
#         return RelationTableEdit
#
# __after_rdf_refactoring__
def get_generic_triple_table(other_entity_class_name, entity_pk_self, detail):

    # TODO RDF : add code from before refactoring and comment it out
    class TripleTableBase(tables.Table):
        """
        The base table from which detail or edit tables will inherit from in order to avoid redundant definitions
        """

        # reuse the logic for ordering and rendering *_date_written
        # Important: The names of these class variables must correspond to the column field name,
        # e.g. for start_date_written, the methods must be named order_start_date_written and render_start_date_written
        order_start_date_written = generic_order_start_date_written
        order_end_date_written = generic_order_end_date_written
        render_start_date_written = generic_render_start_date_written
        render_end_date_written = generic_render_end_date_written

        class Meta:

            # TODO __sresch__ : investigate if it's feasible to have different subclasses of triples and have them
            #  fill in these fields of this Table class automatically

            from apis_core.apis_relations.models import TempTriple

            model = TempTriple

            # the fields list also serves as the defining order of them, as to avoid duplicated definitions
            fields = [
                "start_date_written",
                "end_date_written",
                "other_prop",
                "other_entity",
            ]
            # reuse the list for ordering
            sequence = tuple(fields)

        def render_other_entity(self, record, value):
            """
            Custom render_FOO method for related entity linking. Since the 'other_related_entity' is a generated annotation
            on the queryset, it does not return the related instance but only the foreign key as the integer it is.
            Thus fetching the related instance is necessary.

            :param record: The 'row' of a queryset, i.e. an entity instance
            :param value: The current column of the row, i.e. the 'other_related_entity' annotation
            :return: related instance
            """

            if value == record.subj.pk:
                return record.subj

            elif value == record.obj.pk:
                return record.obj

            else:
                raise Exception(
                    "Did not find the entity this relation is supposed to come from!"
                    + "Something must have went wrong when annotating for the related instance."
                )

        def __init__(self, data, *args, **kwargs):

            # __before_rdf_refactoring__
            #
            # # annotations for displaying data about the 'other side' of the relation.
            # # Both of them ('other_related_entity' and 'other_relation_type') are necessary for displaying relations
            # # in context to what entity we are calling this from.
            # data = data.annotate(
            #     # In order to provide the 'other instance' for each instance of a table where this whole logic is called from,
            #     # the queryset must be annotated accordingly. The following Case searches which of the two related instances
            #     # of a relation queryset entry is the one corresponding to the current entity instance. When found, take the
            #     # other related entity (since this is the one we are interested in displaying).
            #     #
            #     # The approach of using queryset's annotate method allows for per-instance case decision and thus
            #     # guarantees that the other related entity is always correctly picked,
            #     # even in case two entities are of the same class.
            #     other_related_entity=Case(
            #         # **kwargs pattern is needed here as the key-value pairs change with each relation class and entity instance.
            #         When(**{
            #             related_entity_field_name_a + "__pk": entity_instance.pk,
            #             "then": related_entity_field_name_b
            #         }),
            #         When(**{
            #             related_entity_field_name_b + "__pk": entity_instance.pk,
            #             "then": related_entity_field_name_a
            #         }),
            #     )
            # ).annotate(
            #     # Get the correct side of the relation type given the current entity instance.
            #     #
            #     # The approach of using queryset's annotate method allows for per-instance case decision and thus
            #     # guarantees that the other related entity is always correctly picked,
            #     # even in case two entities are of the same class.
            #     other_relation_type=Case(
            #         When(**{
            #             # A->B relation and current entity instance is A, hence take forward name
            #             related_entity_field_name_a + "__pk": entity_instance.pk,
            #             "then": "relation_type__name"
            #         }),
            #         When(**{
            #             # A->B relation and current entity instance is B, hence take reverse name.
            #             related_entity_field_name_b + "__pk": entity_instance.pk,
            #             "then": "relation_type__name_reverse"
            #         }),
            #     )
            # )
            # for an in data:
            #     if getattr(an, f"{related_entity_field_name_a}_id") == entity_instance.pk:
            #         an.other_relation_type = getattr(an.relation_type, "label")
            #     else:
            #         an.other_relation_type = getattr(an.relation_type, "label_reverse")
            #
            #
            # super().__init__(data, *args, **kwargs)
            #
            # __after_rdf_refactoring__
            data = data.annotate(
                other_entity=Case(
                    # **kwargs pattern is needed here as the key-value pairs change with each relation class and entity instance.
                    When(**{"subj__pk": entity_pk_self, "then": "obj"}),
                    When(**{"obj__pk": entity_pk_self, "then": "subj"}),
                ),
                other_prop=Case(
                    # **kwargs pattern is needed here as the key-value pairs change with each relation class and entity instance.
                    When(**{"subj__pk": entity_pk_self, "then": "prop__name"}),
                    When(**{"obj__pk": entity_pk_self, "then": "prop__name_reverse"}),
                ),
            )

            self.base_columns["other_prop"].verbose_name = "Other property"
            self.base_columns[
                "other_entity"
            ].verbose_name = f"Related {other_entity_class_name.title()}"

            super().__init__(data, *args, **kwargs)

    if detail:

        class TripleTableDetail(TripleTableBase):
            """
            Sublcass inheriting the bulk of logic from parent. This table is used for the 'detail' views.
            """

            def __init__(self, data, *args, **kwargs):

                # __before_rdf_refactoring__
                #
                # # Only addition with respect to parent class is which main url is to be used when clicking on a
                # # related entity column.
                # self.base_columns["other_related_entity"] = tables.LinkColumn(
                #     'apis:apis_entities:generic_entities_detail_view',
                #     args=[
                #         other_related_entity_class_name,
                #         A("other_related_entity")
                #     ],
                #     verbose_name="Related " + other_related_entity_class_name.title()
                # )
                #
                # super().__init__(data=data, *args, **kwargs)
                #
                # __after_rdf_refactoring__
                self.base_columns["other_entity"] = tables.LinkColumn(
                    "apis:apis_entities:generic_entities_detail_view",
                    args=[other_entity_class_name, A("other_entity")],
                )

                super().__init__(data=data, *args, **kwargs)

        return TripleTableDetail

    else:

        class TripleTableEdit(TripleTableBase):
            """
            Sublcass inheriting the bulk of logic from parent. This table is used for the 'edit' view.
            """

            class Meta(TripleTableBase.Meta):
                """
                Additional Meta fields are necessary for editing functionalities
                """

                # This fields list also defines the order of the elements.
                fields = ["delete"] + TripleTableBase.Meta.fields + ["edit"]

                if "apis_bibsonomy" in settings.INSTALLED_APPS:
                    fields = ["ref"] + fields

                # again reuse the fields list for ordering
                sequence = tuple(fields)

            def __init__(self, *args, **kwargs):

                # __before_rdf_refactoring__ TODO RDF:
                #
                # # Clicking on a related entity will lead also the edit view of the related entity instance
                # self.base_columns["other_related_entity"] = tables.LinkColumn(
                #     'apis:apis_entities:generic_entities_edit_view',
                #     args=[
                #         other_related_entity_class_name, A("other_related_entity")
                #     ],
                #     verbose_name="Related " + other_related_entity_class_name.title()
                # )
                #
                # # delete button
                # self.base_columns['delete'] = tables.TemplateColumn(
                #     template_name='apis_relations/delete_button_generic_ajax_form.html'
                # )
                #
                # # edit button
                # self.base_columns['edit'] = tables.TemplateColumn(
                #     template_name='apis_relations/edit_button_generic_ajax_form.html'
                # )
                #
                # # bibsonomy button
                # if 'apis_bibsonomy' in settings.INSTALLED_APPS:
                #     self.base_columns['ref'] = tables.TemplateColumn(
                #         template_name='apis_relations/references_button_generic_ajax_form.html'
                #     )
                #
                # super().__init__(*args, **kwargs)
                #
                # __after_rdf_refactoring__
                # linking entity
                self.base_columns["other_entity"] = tables.LinkColumn(
                    "apis:apis_entities:generic_entities_edit_view",
                    args=[other_entity_class_name, A("other_entity")],
                )

                # edit button
                self.base_columns["edit"] = tables.TemplateColumn(
                    template_name="apis_relations/edit_button_generic_ajax_form.html"
                )

                # delete button
                self.base_columns["delete"] = tables.TemplateColumn(
                    template_name="apis_relations/delete_button_generic_ajax_form.html"
                )
                # bibsonomy button
                if "apis_bibsonomy" in settings.INSTALLED_APPS:
                    self.base_columns["ref"] = tables.TemplateColumn(
                        template_name="apis_relations/references_button_generic_ajax_form.html"
                    )

                super().__init__(*args, **kwargs)

        return TripleTableEdit


class EntityUriTable(tables.Table):

    delete = tables.TemplateColumn(
        template_name="apis_relations/delete_button_Uri_ajax_form.html"
    )

    class Meta:
        empty_text = empty_text_default
        model = Uri
        fields = ["uri"]
        sequence = ("delete", "uri")
        # add class="paleblue" to <table> tag
        attrs = {
            "class": "table table-hover table-striped table-condensed",
            "id": "PURI_conn",
        }


class LabelTableBase(tables.Table):

    label2 = tables.TemplateColumn(template_name="apis_relations/labels_label.html")

    # reuse the logic for ordering and rendering *_date_written
    # Important: The names of these class variables must correspond to the column field name,
    # e.g. for start_date_written, the methods must be named order_start_date_written and render_start_date_written
    order_start_date_written = generic_order_start_date_written
    order_end_date_written = generic_order_end_date_written
    render_start_date_written = generic_render_start_date_written
    render_end_date_written = generic_render_end_date_written

    class Meta:

        empty_text = empty_text_default
        model = Label

        # Note that as the next attribute 'sequence' builds on this list 'fields', the order defined within this list
        # will be reused for the tuple 'sequence'. So if the order needs to be changed, better do it here in the list 'fields'.
        fields = [
            "start_date_written",
            "end_date_written",
            "label_type",
            "isoCode_639_3",
        ]
        sequence = ("label2",) + tuple(fields)

        # add class="paleblue" to <table> tag
        attrs = {
            "class": "table table-hover table-striped table-condensed",
            "id": "PL_conn",
        }


class LabelTableEdit(LabelTableBase):
    """
    Reuse most of the base table class for labels. Only addition is editing functionality.
    """

    edit = tables.TemplateColumn(
        template_name="apis_relations/edit_button_persLabel_ajax_form.html"
    )

    class Meta(LabelTableBase.Meta):
        sequence = LabelTableBase.Meta.sequence + ("edit",)
