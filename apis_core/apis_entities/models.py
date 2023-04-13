import re
import re
import unicodedata

from django.contrib.contenttypes.models import ContentType
from django.apps import apps
import reversion
from django.conf import settings
from django.contrib.auth.models import Group
from django.db import models
from django.db.models.signals import m2m_changed, post_save
from django.dispatch import receiver
from django.urls import reverse
from guardian.shortcuts import assign_perm, remove_perm
from model_utils.managers import InheritanceManager
from django.db.models.query import QuerySet

from apis_core.utils import caching
from apis_core.utils import DateParser
from apis_core.apis_metainfo.models import RootObject, Collection
from apis_core.apis_relations.models import TempTriple

BASE_URI = getattr(settings, "APIS_BASE_URI", "http://apis.info/")
NEXT_PREV = getattr(settings, "APIS_NEXT_PREV", True)


class AbstractEntity(RootObject):
    """
    Abstract super class which encapsulates common logic between the
    different entity kinds and provides various methods relating to either
    all or one specific entity kind.

    Most of the class methods are designed to be used in the subclass as they
    are considering contexts which depend on the subclass entity type.
    So they are to be understood in that dynamic context.
    """

    entity_settings = {
        "list_filters": ["name", "related_entity_name", "related_property_name"],
        "search": ["name"],
    }

    class Meta:
        abstract = True

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def __str__(self):
        if self.name != "":
            return self.name
        else:
            return "no name provided"

    @classmethod
    def get_or_create_uri(cls, uri):
        uri = str(uri)
        try:
            if re.match(r"^[0-9]*$", uri):
                p = cls.objects.get(pk=uri)
            else:
                p = cls.objects.get(uri__uri=uri)
            return p
        except:
            print("Found no object corresponding to given uri.")
            return False

    # TODO
    @classmethod
    def get_entity_list_filter(cls):
        return None


@reversion.register()
class TempEntityClass(AbstractEntity):
    """
    Base class to bind common attributes to many classes.

    The common attributes are:
    - written start and enddates,
    - recognized start and enddates which are derived from the written dates
    using RegEx,
    - a review boolean field to mark an object as reviewed.
    """

    review = models.BooleanField(
        default=False,
        help_text="Should be set to True, if the "
        "data record holds up quality "
        "standards.",
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
    # TODO RDF: Make Text also a Subclass of RootObject
    text = models.ManyToManyField("apis_metainfo.Text", blank=True)
    collection = models.ManyToManyField("apis_metainfo.Collection")
    status = models.CharField(max_length=100)
    source = models.ForeignKey(
        "apis_metainfo.Source", blank=True, null=True, on_delete=models.SET_NULL
    )
    references = models.TextField(blank=True, null=True)
    notes = models.TextField(blank=True, null=True)
    published = models.BooleanField(default=False)
    objects = models.Manager()
    objects_inheritance = InheritanceManager()

    def __str__(self):
        if self.name != "" and hasattr(
            self, "first_name"  # TODO RDF: remove first_name here
        ):  # relation usually don´t have names
            return "{}, {} (ID: {})".format(self.name, self.first_name, self.id)
        elif self.name != "":
            return "{} (ID: {})".format(self.name, self.id)
        else:
            return "(ID: {})".format(self.id)

    def save(self, parse_dates=True, *args, **kwargs):
        """
        Adaption of the save() method of the class to automatically parse
        string-dates into date objects.
        """

        if parse_dates:

            # overwrite every field with None as default
            start_date = None
            start_start_date = None
            start_end_date = None
            end_date = None
            end_start_date = None
            end_end_date = None

            # if some textual user input of a start date is there, parse it
            if self.start_date_written:
                start_date, start_start_date, start_end_date = DateParser.parse_date(
                    self.start_date_written
                )

            # if some textual user input of an end date is there, parse it
            if self.end_date_written:
                end_date, end_start_date, end_end_date = DateParser.parse_date(
                    self.end_date_written
                )

            self.start_date = start_date
            self.start_start_date = start_start_date
            self.start_end_date = start_end_date
            self.end_date = end_date
            self.end_start_date = end_start_date
            self.end_end_date = end_end_date

        if self.name:
            self.name = unicodedata.normalize("NFC", self.name)

        super(TempEntityClass, self).save(*args, **kwargs)

        return self

    # TODO RDF: I don't remember what this function was used for.
    #  Investigate or delete it.
    def get_child_entity(self):
        for x in [x for x in apps.all_models["apis_entities"].values()]:
            if x.__name__ in list(settings.APIS_ENTITIES.keys()):
                try:
                    my_ent = x.objects.get(id=self.id)
                    return my_ent
                    break
                except ObjectDoesNotExist:
                    pass
        return None

    @classmethod
    def get_listview_url(self):
        entity = self.__name__.lower()
        return reverse(
            "apis_core:apis_entities:generic_entities_list",
            kwargs={"entity": entity},
        )

    @classmethod
    def get_createview_url(self):
        entity = self.__name__.lower()
        return reverse(
            "apis_core:apis_entities:generic_entities_create_view",
            kwargs={"entity": entity},
        )

    def get_edit_url(self):
        entity = self.__class__.__name__.lower()
        return reverse(
            "apis_core:apis_entities:generic_entities_edit_view",
            kwargs={"entity": entity, "pk": self.id},
        )

    def get_child_class(self):
        child = self.get_child_entity()
        if child:
            return "{}".format(child.__class__.__name__)
        else:
            return "{}".format(child.__class__.__name__)

    def get_absolute_url(self):
        entity = self.__class__.__name__.lower()
        # TODO RDF: Check if this should be removed or adapted
        #
        # if entity == "institution" or len(entity) < 10:
        #     return reverse(
        #         "apis_core:apis_entities:generic_entities_detail_view",
        #         kwargs={"entity": entity, "pk": self.id},
        #     )
        # elif entity == "tempentityclass":
        #     return self.get_child_entity().get_absolute_url()
        # else:
        #     return reverse(
        #         "apis_core:apis_relations:generic_relations_detail_view",
        #         kwargs={"entity": entity, "pk": self.id},
        #     )
        # __after_rdf_refactoring__
        return reverse(
            "apis_core:apis_entities:generic_entities_detail_view",
            kwargs={"entity": entity, "pk": self.id},
        )

    def get_prev_url(self):
        entity = self.__class__.__name__.lower()
        if NEXT_PREV:
            prev = self.__class__.objects.filter(id__lt=self.id).order_by("-id")
        else:
            return False
        if prev:
            return reverse(
                "apis_core:apis_entities:generic_entities_detail_view",
                kwargs={"entity": entity, "pk": prev.first().id},
            )
        else:
            return False

    def get_next_url(self):
        entity = self.__class__.__name__.lower()
        if NEXT_PREV:
            next = self.__class__.objects.filter(id__gt=self.id)
        else:
            return False
        if next:
            return reverse(
                "apis_core:apis_entities:generic_entities_detail_view",
                kwargs={"entity": entity, "pk": next.first().id},
            )
        else:
            return False

    def get_delete_url(self):
        entity = self.__class__.__name__.lower()
        return reverse(
            "apis_core:apis_entities:generic_entities_delete_view",
            kwargs={"entity": entity, "pk": self.id},
        )

    def get_duplicate_url(self):
        entity = self.__class__.__name__.lower()
        return reverse(
            "apis_core:apis_entities:generic_entities_duplicate_view",
            kwargs={"entity": entity, "pk": self.id},
        )

    def merge_with(self, entities):
        # TODO: check if these imports can be put to top of module without
        #  causing circular import issues.
        from apis_core.apis_labels.models import Label
        from apis_core.apis_vocabularies.models import LabelType
        from apis_core.apis_metainfo.models import Uri

        e_a = type(self).__name__
        self_model_class = ContentType.objects.get(model__iexact=e_a).model_class()
        if isinstance(entities, int):
            entities = self_model_class.objects.get(pk=entities)
        if not isinstance(entities, list) and not isinstance(entities, QuerySet):
            entities = [entities]
            entities = [
                self_model_class.objects.get(pk=ent) if type(ent) == int else ent
                for ent in entities
            ]
        for ent in entities:
            e_b = type(ent).__name__
            if e_a != e_b:
                continue
            lt, created = LabelType.objects.get_or_create(name="Legacy name (merge)")
            col_list = list(self.collection.all())
            for col2 in ent.collection.all():
                if col2 not in col_list:
                    self.collection.add(col2)
            for f in ent._meta.local_many_to_many:
                if not f.name.endswith("_set"):
                    sl = list(getattr(self, f.name).all())
                    for s in getattr(ent, f.name).all():
                        if s not in sl:
                            getattr(self, f.name).add(s)
            Label.objects.create(label=str(ent), label_type=lt, temp_entity=self)
            for u in Uri.objects.filter(root_object=ent):
                u.entity = self
                u.save()
            for l in Label.objects.filter(temp_entity=ent):
                l.temp_entity = self
                l.save()
            TempTriple.objects.filter(obj__id=ent.id).update(obj=self)
            TempTriple.objects.filter(subj__id=ent.id).update(subj=self)
            ent.delete()

    def get_serialization(self):
        from apis_core.apis_entities.serializers_generic import EntitySerializer

        return EntitySerializer(self).data


def prepare_fields_dict(fields_list, vocabs, vocabs_m2m):
    res = dict()
    for f in fields_list:
        res[f["name"]] = getattr(models, f["field_type"])(**f["attributes"])
    for v in vocabs:
        res[v] = models.ForeignKey(
            f"apis_vocabularies.{v}", blank=True, null=True, on_delete=models.SET_NULL
        )
    for v2 in vocabs_m2m:
        res[v2] = models.ManyToManyField(f"apis_vocabularies.{v2}", blank=True)
    return res


# ents_cls_list = []
# if a_ents:
#     with open(a_ents, "r") as ents_file:
#         ents = yaml.load(ents_file, Loader=yaml.CLoader)
#         print(ents)
#         for ent in ents["entities"]:
#             attributes = prepare_fields_dict(
#                 ent["fields"], ent.get("vocabs", []), ent.get("vocabs_m2m", [])
#             )
#             attributes["__module__"] = __name__
#             ent_class = type(ent["name"], (AbstractEntity,), attributes)
#             globals()[ent["name"]] = ent_class
#             ents_cls_list.append(ent_class)
#             reversion.register(ent_class, follow=["tempentityclass_ptr"])


@receiver(post_save, dispatch_uid="create_default_uri")
def create_default_uri(sender, instance, **kwargs):
    from apis_core.apis_metainfo.models import Uri

    if kwargs["created"] and sender in caching.get_all_ontology_classes():
        if BASE_URI.endswith("/"):
            base1 = BASE_URI[:-1]
        else:
            base1 = BASE_URI
        uri_c = "{}{}".format(
            base1,
            reverse("GetEntityGenericRoot", kwargs={"pk": instance.pk}),
        )
        uri2 = Uri(uri=uri_c, domain="apis default", root_object=instance)
        uri2.save()


lst_entities_complete = [
    globals()[x]
    for x in globals()
    if isinstance(globals()[x], models.base.ModelBase)
    and globals()[x].__module__ == "apis_core.apis_entities.models"
    and x != "AbstractEntity"
    and globals()[x]
]
lst_entities_complete = list(dict.fromkeys(lst_entities_complete))

# TODO: inspect.
#  This list here will contain only duplicates if
#  `lst_entities_complete` contains all entities
perm_change_senders = [
    getattr(getattr(x, "collection"), "through") for x in lst_entities_complete
]


@receiver(
    m2m_changed,
    dispatch_uid="create_object_permissions",
)
def create_object_permissions(sender, instance, **kwargs):
    if kwargs["action"] == "pre_add" and sender in perm_change_senders:
        perms = []
        for j in kwargs["model"].objects.filter(pk__in=kwargs["pk_set"]):
            perms.extend(j.groups_allowed.all())
        for x in perms:
            assign_perm("change_" + instance.__class__.__name__.lower(), x, instance)
            assign_perm("delete_" + instance.__class__.__name__.lower(), x, instance)
    elif kwargs["action"] == "post_remove" and sender in perm_change_senders:
        perms = []
        perms_keep = []
        for j in kwargs["model"].objects.filter(pk__in=kwargs["pk_set"]):
            perms.extend(j.groups_allowed.all())
        for u in instance.collection.all():
            perms_keep.extend(u.groups_allowed.all())
        rm_perms = set(perms) - set(perms_keep)
        for x in rm_perms:
            remove_perm("change_" + instance.__class__.__name__.lower(), x, instance)
            remove_perm("delete_" + instance.__class__.__name__.lower(), x, instance)


@receiver(
    m2m_changed,
    sender=Collection.groups_allowed.through,
    dispatch_uid="add_usergroup_collection",
)
def add_usergroup_collection(sender, instance, **kwargs):
    if kwargs["action"] == "pre_add":
        for x in kwargs["model"].objects.filter(pk__in=kwargs["pk_set"]):
            for z in ["change", "delete"]:
                for y in [Person, Institution, Place, Event, Work]:
                    assign_perm(
                        z + "_" + y.__name__.lower(),
                        x,
                        y.objects.filter(collection=instance),
                    )


if "registration" in getattr(settings, "INSTALLED_APPS", []):
    from registration.backends.simple.views import RegistrationView
    from registration.signals import user_registered

    @receiver(
        user_registered,
        sender=RegistrationView,
        dispatch_uid="add_registered_user_to_group",
    )
    def add_user_to_group(sender, user, request, **kwargs):
        user_group = getattr(settings, "APIS_AUTO_USERGROUP", None)
        if user_group is not None:
            user.groups.add(Group.objects.get(name=user_group))


# TODO remove this workaround here once the settings issue is resolved
def fill_settings_with_entity_attributes():
    if not settings.APIS_ENTITIES:
        for entity_class in (
            caching.get_all_entity_classes() + caching.get_all_ontology_classes()
        ):
            entity_settings = entity_class.entity_settings
            settings.APIS_ENTITIES[entity_class.__name__] = entity_settings


fill_settings_with_entity_attributes()
