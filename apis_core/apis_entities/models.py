import functools
import logging
import re
import ast

from django.conf import settings
from django.contrib.contenttypes.fields import GenericRelation
from django.contrib.contenttypes.models import ContentType
from django.db.models.base import ModelBase
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.urls import NoReverseMatch, reverse

from apis_core.apis_metainfo.models import RootObject, Uri
from apis_core.utils.settings import apis_base_uri

NEXT_PREV = getattr(settings, "APIS_NEXT_PREV", True)

logger = logging.getLogger(__name__)


def proc_ast_node(node, res):
    for ent in node.body:
        if isinstance(ent, ast.Assign):
            match ent.targets[0].id:
                case "subj_model":
                    res["forward"].setdefault(ent.value.id, []).append(node.name)
                case "obj_model":
                    res["reverse"].setdefault(ent.value.id, []).append(node.name)
    return res


@functools.cache
def get_relations_from_module(module):
    res = {"forward": {}, "reverse": {}}
    imp_path = "/".join(module.split(".")) + ".py"
    with open(imp_path, "r") as inp:
        tree = ast.parse(inp.read())
        for node in ast.walk(tree):
            if not isinstance(node, ast.ClassDef):
                continue
            base_cls = [
                cl.id.lower() if hasattr(cl, "id") else None for cl in node.bases
            ]
            if not "relation" in base_cls:
                continue
            res = proc_ast_node(node, res)
    return res


class AbstractEntityModelBase(ModelBase):
    def __new__(metacls, name, bases, attrs):
        base_cls = [cl._meta.model_name for cl in bases]
        if "abstractentity" in base_cls:
            dict_cls = get_relations_from_module(attrs["__module__"])
            if name in dict_cls["forward"]:
                for cl in dict_cls["forward"][name]:
                    attrs[f"rel_{cl.lower()}"] = GenericRelation(
                        cl,
                        object_id_field="subj_object_id",
                        content_type_field="subj_content_type",
                    )
            if name in dict_cls["reverse"]:
                for cl in dict_cls["reverse"][name]:
                    attrs[f"rel_rev_{cl.lower()}"] = GenericRelation(
                        cl,
                        object_id_field="obj_object_id",
                        content_type_field="obj_content_type",
                    )
        if name == "AbstractEntity":
            return super().__new__(metacls, name, bases, attrs)
        else:
            new_class = super().__new__(metacls, name, bases, attrs)
            if not new_class._meta.ordering:
                logger.warning(
                    f"{name} inherits from AbstractEntity but does not specify 'ordering' in its Meta class. "
                    "Empty ordering could result in inconsitent results with pagination. "
                    "Set a ordering or inherit the Meta class from AbstractEntity.",
                )

            return new_class


class AbstractEntity(RootObject, metaclass=AbstractEntityModelBase):
    """
    Abstract super class which encapsulates common logic between the
    different entity kinds and provides various methods relating to either
    all or one specific entity kind.

    Most of the class methods are designed to be used in the subclass as they
    are considering contexts which depend on the subclass entity type.
    So they are to be understood in that dynamic context.
    """

    class Meta:
        abstract = True

    @classmethod
    def get_or_create_uri(cls, uri):
        uri = str(uri)
        try:
            if re.match(r"^[0-9]*$", uri):
                p = cls.objects.get(pk=uri)
            else:
                p = cls.objects.get(uri__uri=uri)
            return p
        except Exception as e:
            print("Found no object corresponding to given uri." + e)
            return False

    # TODO
    @classmethod
    def get_entity_list_filter(cls):
        return None

    @functools.cached_property
    def get_prev_id(self):
        if NEXT_PREV:
            prev_instance = (
                type(self)
                .objects.filter(id__lt=self.id)
                .order_by("-id")
                .only("id")
                .first()
            )
            if prev_instance is not None:
                return prev_instance.id
        return False

    @functools.cached_property
    def get_next_id(self):
        if NEXT_PREV:
            next_instance = (
                type(self)
                .objects.filter(id__gt=self.id)
                .order_by("id")
                .only("id")
                .first()
            )
            if next_instance is not None:
                return next_instance.id
        return False


@receiver(post_save, dispatch_uid="create_default_uri")
def create_default_uri(sender, instance, created, raw, using, update_fields, **kwargs):
    # disable the handler during fixture loading
    if raw:
        return
    create_default_uri = getattr(settings, "CREATE_DEFAULT_URI", True)
    skip_default_uri = getattr(instance, "skip_default_uri", False)
    if create_default_uri and not skip_default_uri:
        if isinstance(instance, AbstractEntity) and created:
            base = apis_base_uri().strip("/")
            try:
                route = reverse("GetEntityGenericRoot", kwargs={"pk": instance.pk})
            except NoReverseMatch:
                route = reverse(
                    "apis_core:GetEntityGeneric", kwargs={"pk": instance.pk}
                )
            uri = f"{base}{route}"
            content_type = ContentType.objects.get_for_model(instance)
            Uri.objects.create(
                uri=uri,
                content_type=content_type,
                object_id=instance.id,
            )
