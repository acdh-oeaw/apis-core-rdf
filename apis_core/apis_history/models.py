from collections.abc import Iterable
from typing import Any
import pytz
from simple_history.models import HistoricalRecords
from django.core.exceptions import AppRegistryNotReady
import inspect
import django
from django.db import models
from apis_core.apis_relations.models import TempTriple
from datetime import datetime
from simple_history import utils
from django.db.models import Q


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


class APISHistoryTableBase(models.Model):
    version_tag = models.CharField(max_length=255, blank=True, null=True)

    class Meta:
        abstract = True

    def get_triples_for_version(self):
        triples = TempTriple.history.as_of(self.history_date).filter(
            Q(subj=self.instance) | Q(obj=self.instance)
        )
        return triples


class VersionMixin(models.Model):
    history = APISHistoricalRecords(inherit=True, bases=[APISHistoryTableBase])
    __history_date = None

    @property
    def _history_date(self):
        return self.__history_date

    @_history_date.setter
    def _history_date(self, value):
        self.__history_date = value

    class Meta:
        abstract = True

    def save(self, *args, **kwargs) -> None:
        if self._history_date is None:
            self._history_date = datetime.now()
        return super().save(*args, **kwargs)

    def __init__(self, *args: Any, **kwargs: Any) -> None:
        super().__init__(*args, **kwargs)
