import dataclasses
import inspect
from typing import Any

import django
from django.conf import settings
from django.contrib.contenttypes.models import ContentType
from django.core.exceptions import AppRegistryNotReady
from django.db import models
from django.db.models import Q
from django.urls import reverse
from django.utils import timezone
from simple_history import utils
from simple_history.models import HistoricalRecords

from apis_core.generic.abc import GenericModel


class APISHistoricalRecords(HistoricalRecords, GenericModel):
    def get_m2m_fields_from_model(self, model):
        # Change the original simple history function to also return m2m fields
        m2m_fields = []
        try:
            for field in inspect.getmembers(model):
                if isinstance(
                    field[1],
                    django.db.models.fields.related_descriptors.ManyToManyDescriptor,
                ):
                    m2m_fields.append(getattr(model, field[0]).field)
        except AppRegistryNotReady:
            pass
        return m2m_fields

    def get_prev_record(self):
        """
        Get the previous history record for the instance. `None` if first.
        """
        history = utils.get_history_manager_from_history(self)
        return (
            history.filter(history_date__lt=self.history_date)
            .order_by("history_date")
            .first()
        )


class APISHistoryTableBase(models.Model, GenericModel):
    class Meta:
        abstract = True

    def get_absolute_url(self):
        ct = ContentType.objects.get_for_model(self)
        return reverse("apis_core:generic:detail", args=[ct, self.history_id])

    def get_reset_url(self):
        ct = ContentType.objects.get_for_model(self)
        return reverse("apis_core:history:reset", args=[ct, self.history_id])

    def _flatten_modelchange_many_to_many(self, obj: Any) -> Any:
        """
        The `.diff_against` method of the `HistoricalChanges` model represent
        changes in many-to-many fields as lists of dicts. Those dicts contain
        a mapping of the model names to the model instances (i.e.
        {'person': <Person1>, 'profession': <Profession2>}).
        To make this a bit more readable, we flatten the dicts to one dict
        containing a mapping between the model instance string representation
        and the string representations of the connected model instances.
        """
        ret = []
        for el in obj:
            key, val = el.values()
            ret.append(str(val))
        return ret

    def get_diff(self, other_version=None):
        if self.history_type == "-":
            return None
        version = other_version or self.prev_record
        if version:
            delta = self.diff_against(version, foreign_keys_are_objs=True)
        else:
            delta = self.diff_against(self.__class__(), foreign_keys_are_objs=True)
        changes = list(
            filter(
                lambda x: (x.new != "" or x.old is not None)
                and x.field != "id"
                and not x.field.endswith("_ptr"),
                delta.changes,
            )
        )
        # The changes consist of `ModelChange` classes, which are frozen
        # To flatten the many-to-many representation of those ModelChanges
        # we use a separate list containing the changed values
        newchanges = []
        m2m_fields = {field.name for field in self.instance_type._meta.many_to_many}
        for change in changes:
            # run flattening only on m2m fields
            if change.field in m2m_fields:
                change = dataclasses.replace(
                    change,
                    old=self._flatten_modelchange_many_to_many(change.old),
                    new=self._flatten_modelchange_many_to_many(change.new),
                )
            newchanges.append(change)
        return sorted(newchanges, key=lambda change: change.field)


class VersionMixin(models.Model):
    history = APISHistoricalRecords(
        inherit=True,
        bases=[
            APISHistoryTableBase,
        ],
        custom_model_name=lambda x: f"Version{x}",
    )
    __history_date = None

    @property
    def _history_date(self):
        return self.__history_date or timezone.now()

    @_history_date.setter
    def _history_date(self, value):
        self.__history_date = value
        pass

    class Meta:
        abstract = True

    def get_history_url(self):
        ct = ContentType.objects.get_for_model(self)
        return reverse("apis_core:history:history", args=[ct, self.id])

    def _get_historical_relations(self):
        ret = []
        if "apis_core.relations" in settings.INSTALLED_APPS:
            from apis_core.relations.utils import relation_content_types

            ct = ContentType.objects.get_for_model(self)

            rel_content_types = relation_content_types(any_model=type(self))
            rel_models = [ct.model_class() for ct in rel_content_types]
            rel_history_models = [
                model for model in rel_models if issubclass(model, VersionMixin)
            ]

            for model in rel_history_models:
                ret.append(
                    model.history.filter(
                        Q(subj_object_id=self.id, subj_content_type=ct)
                        | Q(obj_object_id=self.id, obj_content_type=ct)
                    ).order_by("history_id")
                )
        return ret

    def get_history_data(self):
        data = []
        prev_entry = None
        queries = self._get_historical_relations()
        flatten_queries = [entry for query in queries for entry in query]

        for entry in flatten_queries:
            if prev_entry is not None:
                if (
                    entry.history_date == prev_entry.history_date
                    and entry.history_user_id == prev_entry.history_user_id
                ):
                    entry.history_type = prev_entry.history_type
                    data[-1] = entry
                    prev_entry = entry
                    continue
            data.append(entry)
            prev_entry = entry
        data += [x for x in self.history.all()]
        data = sorted(data, key=lambda x: x.history_date, reverse=True)
        return data

    def __init__(self, *args: Any, **kwargs: Any) -> None:
        super().__init__(*args, **kwargs)
