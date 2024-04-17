from apis_core.apis_metainfo.models import RootObject
from django.db import models
from django.db.models.base import ModelBase
from django.core.exceptions import ValidationError
from model_utils.managers import InheritanceManager


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


class Relation(models.Model, metaclass=RelationModelBase):
    subj = models.ForeignKey(
        RootObject,
        on_delete=models.SET_NULL,
        null=True,
        related_name="relations_as_subj",
    )
    obj = models.ForeignKey(
        RootObject,
        on_delete=models.SET_NULL,
        null=True,
        related_name="relations_as_obj",
    )

    objects = InheritanceManager()

    def save(self, *args, **kwargs):
        if self.subj:
            subj = RootObject.objects_inheritance.get_subclass(id=self.subj.id)
            if not type(subj) in self.subj_list():
                raise ValidationError(
                    f"{self.subj} is not of any type in {self.subj_model}"
                )
        if self.obj:
            obj = RootObject.objects_inheritance.get_subclass(id=self.obj.id)
            if not type(obj) in self.obj_list():
                raise ValidationError(
                    f"{self.obj} is not of any type in {self.obj_model}"
                )
        super().save(*args, **kwargs)

    @property
    def subj_to_obj_text(self):
        if hasattr(self, "name"):
            return f"{self.subj} {self.name} {self.obj}"
        return f"{self.subj} relation to {self.obj}"

    @property
    def obj_to_subj_text(self):
        if hasattr(self, "reverse_name"):
            return f"{self.subj} {self.reverse_name} {self.obj}"
        return f"{self.obj} relation to {self.subj}"

    def __str__(self):
        return self.subj_to_obj_text

    @classmethod
    def is_subj(cls, something):
        return something in cls.subj_list()

    @classmethod
    def is_obj(cls, something):
        return something in cls.obj_list()

    @classmethod
    def subj_list(cls):
        return cls.subj_model if isinstance(cls.subj_model, list) else [cls.subj_model]

    @classmethod
    def obj_list(cls):
        return cls.obj_model if isinstance(cls.obj_model, list) else [cls.obj_model]

    def clean(self):
        if self.subj:
            subj = RootObject.objects_inheritance.get_subclass(id=self.subj.id)
            if not type(subj) in self.subj_list():
                raise ValidationError(
                    f"{self.subj} is not of any type in {self.subj_model}"
                )
        if self.obj:
            obj = RootObject.objects_inheritance.get_subclass(id=self.obj.id)
            if not type(obj) in self.obj_list():
                raise ValidationError(
                    f"{self.obj} is not of any type in {self.obj_model}"
                )
