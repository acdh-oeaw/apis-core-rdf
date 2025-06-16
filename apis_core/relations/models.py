import functools
import logging

from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.core.exceptions import ValidationError
from django.db import models
from django.db.models.base import ModelBase
from model_utils.managers import InheritanceManager

from apis_core.generic.abc import GenericModel

logger = logging.getLogger(__name__)


# This ModelBase is simply there to check if the needed attributes
# are set in the Relation child classes.
class RelationModelBase(ModelBase):
    def __new__(metacls, name, bases, attrs):
        if name == "Relation":
            return super().__new__(metacls, name, bases, attrs)
        else:
            new_class = super().__new__(metacls, name, bases, attrs)
            if not (new_class._meta.abstract or new_class._meta.proxy):
                if not hasattr(new_class, "subj_model"):
                    raise ValueError(
                        "%s inherits from Relation and must therefore specify subj_model"
                        % name
                    )
                if not hasattr(new_class, "obj_model"):
                    raise ValueError(
                        "%s inherits from Relation and must therefore specify obj_model"
                        % name
                    )

                # `subj_model` or `obj_model` being a list was supported in an earlier
                # version of apis, but it is not anymore
                if isinstance(getattr(new_class, "subj_model", None), list):
                    raise ValueError("%s.subj_model must not be a list" % name)
                if isinstance(getattr(new_class, "obj_model", None), list):
                    raise ValueError("%s.obj_model mut not be a list" % name)

            if not new_class._meta.ordering:
                logger.warning(
                    f"{name} inherits from Relation but does not specify 'ordering' in its Meta class. "
                    "Empty ordering could result in inconsitent results with pagination. "
                    "Set a ordering or inherit the Meta class from Relation.",
                )

            return new_class


@functools.cache
def get_by_natural_key(natural_key: str):
    app_label, name = natural_key.lower().split(".")
    return ContentType.objects.get_by_natural_key(app_label, name).model_class()


class Relation(models.Model, GenericModel, metaclass=RelationModelBase):
    subj_content_type = models.ForeignKey(
        ContentType, on_delete=models.CASCADE, related_name="relation_subj_set"
    )
    subj_object_id = models.PositiveIntegerField(null=True)
    subj = GenericForeignKey("subj_content_type", "subj_object_id")
    obj_content_type = models.ForeignKey(
        ContentType, on_delete=models.CASCADE, related_name="relation_obj_set"
    )
    obj_object_id = models.PositiveIntegerField(null=True)
    obj = GenericForeignKey("obj_content_type", "obj_object_id")

    objects = InheritanceManager()

    def save(self, *args, **kwargs):
        if self.subj_content_type:
            if self.subj_content_type.model_class() not in self.subj_list():
                raise ValidationError(
                    f"{self.subj} is not of any type in {self.subj_list()}"
                )
        if self.obj_content_type:
            if self.obj_content_type.model_class() not in self.obj_list():
                raise ValidationError(
                    f"{self.obj} is not of any type in {self.obj_list()}"
                )
        super().save(*args, **kwargs)

    @property
    def subj_to_obj_text(self) -> str:
        if hasattr(self, "name"):
            return f"{self.subj} {self.name()} {self.obj}"
        return f"{self.subj} relation to {self.obj}"

    @property
    def obj_to_subj_text(self) -> str:
        if hasattr(self, "reverse_name"):
            return f"{self.obj} {self.reverse_name()} {self.subj}"
        return f"{self.obj} relation to {self.subj}"

    def __str__(self):
        return self.subj_to_obj_text

    @classmethod
    def _get_models(cls, model):
        models = model if isinstance(model, list) else [model]
        return [
            get_by_natural_key(model) if isinstance(model, str) else model
            for model in models
        ]

    @classmethod
    def subj_list(cls) -> list[models.Model]:
        return cls._get_models(cls.subj_model)

    @classmethod
    def obj_list(cls) -> list[models.Model]:
        return cls._get_models(cls.obj_model)

    @classmethod
    def name(cls) -> str:
        return cls._meta.verbose_name

    @classmethod
    def reverse_name(cls) -> str:
        return cls._meta.verbose_name + " reverse"
