import inspect
from datetime import datetime
from typing import Any

import django
from django.conf import settings
from django.contrib.contenttypes.models import ContentType
from django.core.exceptions import AppRegistryNotReady
from django.db import models
from django.db.models import Q, UniqueConstraint
from django.db.models.functions import Lower
from django.urls import reverse
from django.utils import timezone
from simple_history import utils
from simple_history.models import HistoricalRecords

from apis_core.apis_metainfo.models import RootObject
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

        if not isinstance(self.instance, RootObject):
            return TempTriple.objects.none()

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

    def get_diff(self, other_version=None):
        if self.history_type == "-":
            return None
        version = other_version or self.prev_record
        if version:
            delta = self.diff_against(version)
        else:
            delta = self.diff_against(self.__class__())
        changes = list(
            filter(
                lambda x: (x.new != "" or x.old is not None)
                and x.field != "id"
                and not x.field.endswith("_ptr"),
                delta.changes,
            )
        )
        return sorted(changes, key=lambda change: change.field)


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

    def get_create_version_url(self):
        ct = ContentType.objects.get_for_model(self)
        return reverse("apis_core:history:add_new_history_version", args=[ct, self.id])

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

    def _get_historical_triples(self):
        # TODO: this is a workaround to filter out Triple history entries and leave
        # TempTriple entries only. Fix when we switch to new relations model.
        ret = []
        if "apis_core.apis_relations" in settings.INSTALLED_APPS:
            from apis_core.apis_relations.models import TempTriple

            ret.append(
                TempTriple.history.filter(Q(subj=self) | Q(obj=self)).order_by(
                    "history_id"
                )
            )
        return ret

    def get_history_data(self):
        data = []
        prev_entry = None
        queries = self._get_historical_relations() + self._get_historical_triples()
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
