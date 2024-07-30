from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.db import models
from django.db.models.base import ModelBase
from django.core.exceptions import ValidationError
from model_utils.managers import InheritanceManager
from apis_core.generic.abc import GenericModel


# This ModelBase is simply there to check if the needed attributes
# are set in the Relation child classes.
class RelationModelBase(ModelBase):
    def __new__(metacls, name, bases, attrs):
        if name == "Relation":
            return super().__new__(metacls, name, bases, attrs)
        else:
            new_class = super().__new__(metacls, name, bases, attrs)
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

            return new_class


class Relation(models.Model, GenericModel, metaclass=RelationModelBase):
    subj_content_type = models.ForeignKey(
        ContentType, on_delete=models.CASCADE, related_name="relation_subj_set"
    )
    subj_object_id = models.PositiveIntegerField()
    subj = GenericForeignKey("subj_content_type", "subj_object_id")
    obj_content_type = models.ForeignKey(
        ContentType, on_delete=models.CASCADE, related_name="relation_obj_set"
    )
    obj_object_id = models.PositiveIntegerField()
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
    def subj_list(cls) -> list[models.Model]:
        return cls.subj_model if isinstance(cls.subj_model, list) else [cls.subj_model]

    @classmethod
    def obj_list(cls) -> list[models.Model]:
        return cls.obj_model if isinstance(cls.obj_model, list) else [cls.obj_model]

    @classmethod
    def name(cls) -> str:
        return cls._meta.verbose_name

    @classmethod
    def reverse_name(cls) -> str:
        return cls._meta.verbose_name + " reverse"
