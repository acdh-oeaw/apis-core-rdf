from typing import Any
from apis_core.generic.abc import GenericModel
from django.urls import reverse
from simple_history.models import HistoricalRecords
from django.core.exceptions import AppRegistryNotReady
import inspect
import django
from django.db import models
from datetime import datetime
from simple_history import utils
from django.db.models import UniqueConstraint, Q
from django.db.models.functions import Lower
from django.contrib.contenttypes.models import ContentType
from django.utils import timezone


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
    version_tag = models.CharField(max_length=255, blank=True, null=True)

    class Meta:
        abstract = True
        constraints = [
            UniqueConstraint(
                fields=["id", Lower("version_tag")], name="id_version_tag_unique"
            ),
        ]

    def get_triples_for_version(
        self,
        only_latest: bool = True,
        history_date: datetime = None,
        filter_for_triples: bool = True,
    ):
        """returns all triples for a specific version of a model instance.
        If only_latest is True, only the latest version of a triple is returned."""
        from apis_core.apis_relations.models import TempTriple

        if history_date is None:
            filter_date = (
                self.next_record.history_date if self.next_record else datetime.now()
            )
        else:
            filter_date = history_date
        triples = TempTriple.history.filter(
            Q(subj=self.instance) | Q(obj=self.instance), history_date__lte=filter_date
        )
        if self.version_tag and filter_for_triples:
            triples = triples.filter(
                Q(version_tag=self.version_tag)
                | Q(version_tag__contains=f"{self.version_tag},")
            )
        if only_latest:
            triples = triples.latest_of_each()
        if filter_for_triples:
            triples = triples.exclude(history_type="-")
        return triples

    def set_version_tag(self, tag: str, include_triples: bool = True):
        self.version_tag = tag
        if include_triples:
            triples = self.get_triples_for_version(filter_for_triples=False)
            for triple in triples:
                if triple.version_tag is None:
                    triple.version_tag = tag
                else:
                    triple.version_tag = f"{triple.version_tag},{tag},".replace(
                        ",,", ","
                    )
                triple.save()
        self.save()

    def get_absolute_url(self):
        ct = ContentType.objects.get_for_model(self)
        return reverse("apis_core:generic:detail", args=[ct, self.history_id])


class VersionMixin(models.Model):
    history = APISHistoricalRecords(
        inherit=True,
        bases=[
            APISHistoryTableBase,
        ],
        custom_model_name=lambda x: f"Version{x}",
        verbose_name="Version",
        verbose_name_plural="Versions",
    )
    __history_date = None

    @property
    def _history_date(self):
        return self.__history_date

    @_history_date.setter
    def _history_date(self, value):
        self.__history_date = value
        pass

    class Meta:
        abstract = True

    def save(self, *args, **kwargs) -> None:
        if self._history_date is None:
            self._history_date = timezone.now()
        return super().save(*args, **kwargs)

    def delete(self, *args, **kwargs) -> tuple[int, dict[str, int]]:
        if self._history_date is None:
            self._history_date = datetime.now()
        return super().delete(*args, **kwargs)

    def get_history_url(self):
        ct = ContentType.objects.get_for_model(self)
        return reverse("apis_core:history:change_history", args=[ct, self.id])

    def get_create_version_url(self):
        ct = ContentType.objects.get_for_model(self)
        return reverse("apis_core:history:add_new_history_version", args=[ct, self.id])

    def get_history_data(self):
        from apis_core.apis_relations.models import TempTriple

        data = []
        prev_entry = None
        # TODO: this is a workaround to filter out Triple history entries and leave
        # TempTriple entries only. Fix when we switch to new relations model.
        for entry in TempTriple.history.filter(
            Q(subj_id=self.id) | Q(obj_id=self.id)
        ).order_by("history_id"):
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
