from django.utils.translation import gettext_lazy as _

from apis_core.apis_entities.abc import E21_Person, E53_Place, E74_Group
from apis_core.relations.models import Relation


class IsMemberOf(Relation):
    subj_model = E21_Person
    obj_model = E74_Group

    class Meta:
        abstract = True

    @classmethod
    def name(self) -> str:
        return _("is member of")

    @classmethod
    def reverse_name(self) -> str:
        return _("has as member")


class LivesIn(Relation):
    subj_model = E21_Person
    obj_model = E53_Place

    class Meta:
        abstract = True

    @classmethod
    def name(self) -> str:
        return _("lives in")

    @classmethod
    def reverse_name(self) -> str:
        return _("has habitant")


class IsLocatedIn(Relation):
    subj_model = E53_Place
    obj_model = E53_Place

    class Meta:
        abstract = True

    @classmethod
    def name(self) -> str:
        return _("is located in")

    @classmethod
    def reverse_name(self) -> str:
        return _("is location of")


class BornIn(Relation):
    subj_model = E21_Person
    obj_model = E53_Place

    class Meta:
        abstract = True

    @classmethod
    def name(self) -> str:
        return _("born in")

    @classmethod
    def reverse_name(self) -> str:
        return _("is birth place of")


class DiedIn(Relation):
    subj_model = E21_Person
    obj_model = E53_Place

    class Meta:
        abstract = True

    @classmethod
    def name(self) -> str:
        return _("died in")

    @classmethod
    def reverse_name(self) -> str:
        return _("is place of death of")
