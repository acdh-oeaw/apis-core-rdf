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
from simple_history.models import HistoricalRecords, ModelChange

from apis_core.generic.abc import GenericModel
from apis_core.generic.templatetags.generic import modeldict


class APISHistoricalRecords(HistoricalRecords):
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


class APISHistoryTableBase(GenericModel, models.Model):
    class Meta:
        abstract = True

    def get_absolute_url(self):
        ct = ContentType.objects.get_for_model(self)
        return reverse("apis_core:generic:detail", args=[ct, self.history_id])

    def get_reset_url(self):
        ct = ContentType.objects.get_for_model(self)
        return reverse("apis_core:history:reset", args=[ct, self.history_id])

    def get_diff(self, other_version=None):
        if self.history_type == "-":
            return None

        new_version_dict = modeldict(self.instance, exclude_noneditable=False)

        old_version = other_version or self.prev_record or None
        old_version_dict = dict()
        if old_version:
            old_version_dict = modeldict(
                old_version.instance, exclude_noneditable=False
            )

        # the `modeldict` method uses the field as a dict key but we are only interested
        # in the `.name` of the field, so lets replace the keys:
        new_version_dict = {key.name: value for key, value in new_version_dict.items()}
        old_version_dict = {key.name: value for key, value in old_version_dict.items()}

        newchanges = []
        for field, value in new_version_dict.items():
            old_value = old_version_dict.pop(field, None)
            if (value or old_value) and value != old_value:
                newchanges.append(ModelChange(field, old_value, value))
        for field, value in old_version_dict.items():
            if value is not None:
                newchanges.append(ModelChange(field, value, None))

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
        ret = set()
        if "apis_core.relations" in settings.INSTALLED_APPS:
            from apis_core.relations.utils import relation_content_types

            ct = ContentType.objects.get_for_model(self)

            rel_content_types = relation_content_types(any_model=type(self))
            rel_models = [ct.model_class() for ct in rel_content_types]
            rel_history_models = [
                model for model in rel_models if issubclass(model, VersionMixin)
            ]

            for model in rel_history_models:
                for historical_relation in model.history.filter(
                    Q(subj_object_id=self.id, subj_content_type=ct)
                    | Q(obj_object_id=self.id, obj_content_type=ct)
                ).order_by("history_id"):
                    ret.add(historical_relation)
        # If there is a newer version of a historical relation, also
        # add it to the set. This can be the case when a relation subject
        # or object was changed and the relation does not point to this
        # object anymore. We still want to show the change to make it
        # clear that the relation does not point to the object anymore.
        for historical_relation in ret.copy():
            if historical_relation.next_record:
                ret.add(historical_relation.next_record)
        return ret

    def get_history_data(self):
        data = []
        prev_entry = None
        queries = self._get_historical_relations()

        for entry in queries:
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
