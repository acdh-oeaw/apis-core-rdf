import copy
import unicodedata

from crum import get_current_request
from django.conf import settings
from django.contrib.contenttypes.models import ContentType
from django.db import models
from django.db.models import Q
from django.db.models.fields.related_descriptors import ForwardManyToOneDescriptor
from django.db.models.signals import m2m_changed
from model_utils.managers import InheritanceManager

from apis_core.apis_metainfo.models import RootObject
from apis_core.generic import signals
from apis_core.generic.abc import GenericModel
from apis_core.history.models import VersionMixin
from apis_core.utils import DateParser


def find_if_user_accepted():
    request = get_current_request()
    if request is not None:
        if request.user.is_authenticated:
            return {}
        else:
            return {"published": True}
    else:
        return {}


class BaseRelationManager(models.Manager):
    def get_queryset(self):
        return RelationPublishedQueryset(self.model, using=self._db)

    def filter_ann_proj(self, request=None, ann_proj=1, include_all=True):
        return self.get_queryset().filter_ann_proj(
            request=request, ann_proj=ann_proj, include_all=include_all
        )

    def filter_for_user(self):
        if hasattr(settings, "APIS_SHOW_ONLY_PUBLISHED"):
            return self.get_queryset().filter_for_user()
        else:
            return self.get_queryset()


class Property(RootObject):
    class Meta:
        verbose_name_plural = "Properties"

    objects = BaseRelationManager()
    property_class_uri = models.CharField(
        max_length=255, verbose_name="Property Class URI", blank=True
    )
    # TODO RDF: Redundancy between name_forward and name, solve this.
    name_forward = models.CharField(
        max_length=255,
        verbose_name="Name forward",
        help_text='Inverse relation like: "is sub-class of" vs. "is super-class of".',
        blank=True,
    )
    # TODO RDF: Maybe rename name to name_subj_to_obj and name_reverse to name_obj_to_subj
    name_reverse = models.CharField(
        max_length=255,
        verbose_name="Name reverse",
        help_text='Inverse relation like: "is sub-class of" vs. "is super-class of".',
        blank=True,
    )
    subj_class = models.ManyToManyField(
        ContentType,
        related_name="property_set_subj",
    )
    obj_class = models.ManyToManyField(
        ContentType,
        related_name="property_set_obj",
    )

    def __str__(self):
        return self.name_forward

    def save(self, *args, **kwargs):
        if self.name_reverse == "":
            self.name_reverse = f"{self.name_forward} [INVERSE]"

        self.name_forward = unicodedata.normalize("NFC", str(self.name_forward))
        self.name_reverse = unicodedata.normalize("NFC", str(self.name_reverse))

        if (update_fields := kwargs.get("update_fields")) is not None:
            if "name_forward" in update_fields and "name_reverse" not in update_fields:
                modified_update_fields = set(update_fields)
                modified_update_fields.add("name_reverse")
                kwargs["update_fields"] = modified_update_fields

        super(Property, self).save(*args, **kwargs)
        return self


# TODO: comment and explain
def subj_or_obj_class_changed(sender, is_subj, **kwargs):
    def cascade_subj_obj_class_to_children(
        contenttype_to_add_or_remove,
        contenttype_already_saved_list,
        subj_or_obj_field_function,
    ):
        def get_all_parents(contenttype_current):
            parent_list = []
            class_current = contenttype_current.model_class()
            for class_parent in class_current.__bases__:
                # TODO: Avoid ContentType DB fetch
                contenttype_parent = ContentType.objects.filter(
                    model=class_parent.__name__
                )
                if len(contenttype_parent) == 1:
                    contenttype_parent = contenttype_parent[0]
                    parent_list.append(contenttype_parent)
                    parent_list.extend(get_all_parents(contenttype_parent))

            return parent_list

        def get_all_children(contenttype_current):
            child_list = []
            class_current = contenttype_current.model_class()
            for class_child in class_current.__subclasses__():
                # TODO: Avoid ContentType DB fetch
                contenttype_child = ContentType.objects.get_for_model(class_child)
                child_list.append(contenttype_child)
                child_list.extend(get_all_children(contenttype_child))

            return child_list

        parent_contenttype_list = get_all_parents(contenttype_to_add_or_remove)
        for parent_contenttype in parent_contenttype_list:
            if parent_contenttype in contenttype_already_saved_list:
                raise Exception(
                    f"Pre-existing parent class found when trying to save or remove a property subject or object class."
                    f" The current class to be saved is '{contenttype_to_add_or_remove.model_class().__name__}',"
                    f" but already saved is '{parent_contenttype.model_class().__name__}'."
                    f" Such a save could potentially be in conflict with an ontology."
                    f" Better save or remove the respective top parent subject or object class from this property."
                )
        children_contenttype_list = get_all_children(contenttype_to_add_or_remove)
        for child_contenttype in children_contenttype_list:
            subj_or_obj_field_function(child_contenttype)

    if kwargs["pk_set"] is not None and len(kwargs["pk_set"]) == 1:
        sending_property = kwargs["instance"]
        if sender == Property.subj_class.through:
            subj_or_obj_field = sending_property.subj_class
        elif sender == Property.obj_class.through:
            subj_or_obj_field = sending_property.obj_class
        else:
            raise Exception
        subj_or_obj_field_function = None
        if kwargs["action"] == "pre_add":
            subj_or_obj_field_function = subj_or_obj_field.add
        elif kwargs["action"] == "post_remove":
            subj_or_obj_field_function = subj_or_obj_field.remove
        if subj_or_obj_field_function is not None:
            cascade_subj_obj_class_to_children(
                contenttype_to_add_or_remove=ContentType.objects.get(
                    pk=min(kwargs["pk_set"])
                ),
                contenttype_already_saved_list=subj_or_obj_field.all(),
                subj_or_obj_field_function=subj_or_obj_field_function,
            )


def subj_class_changed(sender, **kwargs):
    subj_or_obj_class_changed(sender, is_subj=True, **kwargs)


def obj_class_changed(sender, **kwargs):
    subj_or_obj_class_changed(sender, is_subj=False, **kwargs)


m2m_changed.connect(subj_class_changed, sender=Property.subj_class.through)
m2m_changed.connect(obj_class_changed, sender=Property.obj_class.through)


class RelationPublishedQueryset(models.QuerySet):
    def filter_for_user(self, *args, **kwargs):
        if getattr(settings, "APIS_SHOW_ONLY_PUBLISHED", False):
            request = get_current_request()
            if request is not None:
                if request.user.is_authenticated:
                    return self
                else:
                    return self.filter(published=True)
            else:
                return self.filter(published=True)
        else:
            return self

    def filter_ann_proj(self, request=None, ann_proj=1, include_all=True):
        """The filter function provided by the manager class.

        :param request: `django.request` object
        :return: queryset that contains only objects that are shown in the highlighted text or those not connected
            to an annotation at all.
        """
        qs = self
        users_show = None
        if request:
            ann_proj = request.session.get("annotation_project", False)
            if not ann_proj:
                return qs
            users_show = request.session.get("users_show_highlighter", None)
        query = Q(annotation__annotation_project_id=ann_proj)
        if users_show is not None:
            query.add(Q(annotation__user_added_id__in=users_show), Q.AND)
        if include_all:
            query.add(Q(annotation__annotation_project__isnull=True), Q.OR)
        return qs.filter(query)


class InheritanceForwardManyToOneDescriptor(ForwardManyToOneDescriptor):
    def get_queryset(self, **hints):
        return self.field.remote_field.model.objects_inheritance.db_manager(
            hints=hints
        ).select_subclasses()


class InheritanceForeignKey(models.ForeignKey):
    forward_related_accessor_class = InheritanceForwardManyToOneDescriptor


class Triple(models.Model, GenericModel):
    subj = InheritanceForeignKey(
        RootObject,
        blank=True,
        null=True,
        on_delete=models.CASCADE,
        related_name="triple_set_from_subj",
        verbose_name="Subject",
    )
    obj = InheritanceForeignKey(
        RootObject,
        blank=True,
        null=True,
        on_delete=models.CASCADE,
        related_name="triple_set_from_obj",
        verbose_name="Object",
    )
    prop = models.ForeignKey(
        Property,
        blank=True,
        null=True,
        on_delete=models.CASCADE,
        related_name="triple_set_from_prop",
        verbose_name="Property",
    )

    objects = BaseRelationManager()
    objects_inheritance = InheritanceManager()

    def __repr__(self):
        try:
            return f"<{self.__class__.__name__}: subj: {self.subj}, prop: {self.prop}, obj: {self.obj}>"
        except RootObject.DoesNotExist:
            return f"<{self.__class__.__name__}: None>"

    def __str__(self):
        return self.__repr__()

    def get_web_object(self):
        return {
            "relation_pk": self.pk,
            "subj": str(self.subj),
            "obj": str(self.obj),
            "prop": self.prop.name_forward,
        }

    def save(self, *args, **kwargs):
        # TODO RDF: Integrate more proper check if subj and obj instances are of valid class as defined in prop.subj_class and prop.obj_class
        # def get_all_parents(cls_current):
        #     parent_list = []
        #     for p in cls_current.__bases__:
        #         parent_list.append(p)
        #         parent_list.extend(get_all_parents(p))
        #     return parent_list

        def get_all_childs(cls_current):
            child_list = []
            for p in cls_current.__subclasses__():
                child_list.append(p)
                child_list.extend(get_all_childs(p))

            return child_list

        if self.subj is None or self.obj is None or self.prop is None:
            raise Exception("subj, obj, or prop is None")
        if self.subj is not None:
            subj_class_name = self.subj.__class__.__name__
            if (
                ContentType.objects.get_for_model(self.subj.__class__)
                not in self.prop.subj_class.all()
            ):
                raise Exception(
                    f"Subject class '{subj_class_name}' is not in valid subject class list of property '{self.prop}'"
                )
        if self.obj is not None:
            obj_class_name = self.obj.__class__.__name__
            if (
                ContentType.objects.get_for_model(model=self.obj.__class__)
                not in self.prop.obj_class.all()
            ):
                raise Exception(
                    f"Object class '{obj_class_name}' is not in valid object class list of property '{self.prop}'"
                )

        super().save(*args, **kwargs)

    def duplicate(self):
        origin = self.__class__
        signals.pre_duplicate.send(sender=origin, instance=self)

        instance = copy.copy(self)

        self.pk = None
        self.id = None
        self._state.adding = True
        duplicate = self.save()

        signals.post_duplicate.send(
            sender=origin, instance=instance, duplicate=duplicate
        )
        return duplicate


class TempTriple(Triple, VersionMixin):
    review = models.BooleanField(
        default=False,
        help_text="Should be set to True, if the data record holds up quality standards.",
    )
    start_date = models.DateField(blank=True, null=True)
    start_start_date = models.DateField(blank=True, null=True)
    start_end_date = models.DateField(blank=True, null=True)
    end_date = models.DateField(blank=True, null=True)
    end_start_date = models.DateField(blank=True, null=True)
    end_end_date = models.DateField(blank=True, null=True)
    start_date_written = models.CharField(
        max_length=255,
        blank=True,
        null=True,
        verbose_name="Start",
    )
    end_date_written = models.CharField(
        max_length=255,
        blank=True,
        null=True,
        verbose_name="End",
    )
    # text = models.ManyToManyField("Text", blank=True)
    # collection = models.ManyToManyField("Collection")
    status = models.CharField(max_length=100)
    # source = models.ForeignKey(
    #     "Source", blank=True, null=True, on_delete=models.SET_NULL
    # )
    references = models.TextField(blank=True, null=True)
    notes = models.TextField(blank=True, null=True)

    def save(self, parse_dates=True, *args, **kwargs):
        """Adaption of the save() method of the class to automatically parse string-dates into date objects"""

        if parse_dates:
            # overwrite every field with None as default
            start_date = None
            start_start_date = None
            start_end_date = None
            end_date = None
            end_start_date = None
            end_end_date = None

            if self.start_date_written:
                # If some textual user input of a start date is there, then parse it

                start_date, start_start_date, start_end_date = DateParser.parse_date(
                    self.start_date_written
                )

            if self.end_date_written:
                # If some textual user input of an end date is there, then parse it

                end_date, end_start_date, end_end_date = DateParser.parse_date(
                    self.end_date_written
                )

            self.start_date = start_date
            self.start_start_date = start_start_date
            self.start_end_date = start_end_date
            self.end_date = end_date
            self.end_start_date = end_start_date
            self.end_end_date = end_end_date

        super().save(*args, **kwargs)

        return self
