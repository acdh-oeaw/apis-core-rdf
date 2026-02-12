import unicodedata

from django.conf import settings
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.contrib.postgres.indexes import GinIndex
from django.contrib.postgres.search import (
    SearchQuery,
    SearchRank,
    SearchVector,
    SearchVectorField,
)
from django.db import models
from django.db.models import Case, F, Field, Q, Value, When
from django.db.models.functions import Greatest
from django.db.models.lookups import PatternLookup

from apis_core.search.utils import get_search_serialization_from_instance

from .utils import split_query_string_for_search


@Field.register_lookup
class ILike(PatternLookup):
    """
    We implement our own `ilike` lookup, because the `icontains`
    lookup uses the sql `UPPER` function and matching functions
    with a lookup index does not work.
    """

    lookup_name = "ilike"

    def as_sql(self, compiler, connection):
        lhs, lhs_params = self.process_lhs(compiler, connection)
        rhs, rhs_params = self.process_rhs(compiler, connection)
        params = lhs_params + rhs_params
        return "%s::text ILIKE %s" % (lhs, rhs), params


class SearchManager(models.Manager):
    def search(self, query_str: str, content_types=[], with_content=False):
        """
        We combine multiple approaches to searching the entries.
        We use the `search_vector` full text search on the title
        and the content_text fields. Any calculated rank that is
        lower than 0.01 is set to 0. We then store the maximum
        value of the title rank times 2 and the content rank. This
        is then used the primary means for ranking.
        Then we look at the individual fields and give them weight
        in the order title -> content_text, each both case-sensitive
        & case insensitive. We match those fields for the whole
        `query_str` as well as the individual parts.
        Those checks are then also used as an overall filter, so only results
        containing those strings are looked at and returned.
        """

        query = super().get_queryset()
        search_config = getattr(settings, "SEARCH_SEARCHQUERY_CONFIG", None)
        search_query = SearchQuery(
            unicodedata.normalize("NFKD", query_str), config=search_config
        )
        query = query.annotate(
            title_rank=SearchRank(F("title_search_vector"), search_query),
            content_rank=Value(0.0),
        )
        if with_content:
            query = query.annotate(
                content_rank=SearchRank(F("content_search_vector"), search_query)
            )
        query = query.annotate(
            title_rank=Case(
                When(title_rank__gt=0.01, then=F("title_rank")), default=Value(0.0)
            )
        )
        query = query.annotate(
            content_rank=Case(
                When(content_rank__gt=0.01, then=F("content_rank")), default=Value(0.0)
            )
        )
        query = query.annotate(frank=Greatest(F("title_rank") * 2, "content_rank"))

        lookups = {
            "title__contains": 10,
            "title__ilike": 9,
        }
        if with_content:
            lookups["content_text__contains"] = 6
            lookups["content_text__ilike"] = 5

        parts = split_query_string_for_search(query_str)
        q = Q()
        w = []

        for idx, part in enumerate(parts):
            for lookup, value in lookups.items():
                q |= Q(**{lookup: part})
                w += [When(**{lookup: part, "then": value - idx})]

        query = query.filter(q).annotate(contains=Case(*w, default=0))

        query = query.order_by("-frank", "-contains", "id")

        if content_types:
            query = query.filter(content_type__in=content_types)
        return query


class SearchEntry(models.Model):
    """
    An entry in the search table pointing to a Django model instance
    """

    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE, null=True)
    object_id = models.PositiveIntegerField(null=True)
    content_object = GenericForeignKey()

    title = models.CharField(max_length=1024)

    content = models.JSONField()

    content_text = models.TextField(null=True)

    title_search_vector = SearchVectorField()
    content_search_vector = SearchVectorField()

    objects = SearchManager()

    class Meta:
        unique_together = ["content_type", "object_id"]
        indexes = [
            models.Index(fields=["content_type", "object_id"]),
            GinIndex(
                name="search_sear_content_text_gin",
                fields=["content_text"],
                opclasses=["gin_trgm_ops"],
            ),
            GinIndex(
                name="search_sear_title_gin",
                fields=["title"],
                opclasses=["gin_trgm_ops"],
            ),
            GinIndex(fields=["title_search_vector"]),
            GinIndex(fields=["content_search_vector"]),
        ]

    @classmethod
    def reindex_model_instance(cls, instance):
        content_type = ContentType.objects.get_for_model(instance)

        title = unicodedata.normalize("NFKD", str(instance))

        serialization = get_search_serialization_from_instance(instance)

        serialization_text = {k: str(v) for k, v in serialization.items() if v}
        content_text = " ".join(serialization_text.values())

        defaults = {
            "title": title,
            "content": serialization,
            "content_text": content_text,
        }
        s, c = cls.objects.update_or_create(
            content_type=content_type, object_id=instance.pk, defaults=defaults
        )
        s.title_search_vector = SearchVector("title", weight="A")
        s.content_search_vector = SearchVector("content_text", weight="A")
        s.save()

    @classmethod
    def delete_by_instance(cls, instance):
        content_type = ContentType.objects.get_for_model(instance)

        cls.objects.filter(content_type=content_type, object_id=instance.pk).delete()
