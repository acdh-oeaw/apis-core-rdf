import functools
import logging
import re

from django.conf import settings
from django.db import models
from django.db.models.base import ModelBase
from model_utils.managers import InheritanceManager

from apis_core.generic.abc import GenericModel

NEXT_PREV = getattr(settings, "APIS_NEXT_PREV", True)

logger = logging.getLogger(__name__)


class EntityModelBase(ModelBase):
    def __new__(metacls, name, bases, attrs):
        if name == "Entity":
            return super().__new__(metacls, name, bases, attrs)
        else:
            new_class = super().__new__(metacls, name, bases, attrs)
            if not new_class._meta.ordering:
                logger.warning(
                    f"{name} inherits from Entity but does not specify 'ordering' in its Meta class. "
                    "Empty ordering could result in inconsitent results with pagination. "
                    "Set a ordering or inherit the Meta class from Entity.",
                )

            return new_class


class Entity(GenericModel, models.Model):
    """
    Entity parent class
    """

    objects = InheritanceManager()

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
