import functools
import operator

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
from django.db.models import Case, F, Field, Q, When
from django.db.models.lookups import PatternLookup
from django.utils.text import slugify

from apis_core.search.utils import get_search_serialization_from_instance


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
        We combine multiple approaches to searching the entries:
        We use the `search_vector` full text search as a primary
        lookup and give all entries that match with a higher rank
        than 0.5 a weight of 1, all the other results get a weight
        of 0.
        Then we look at the individiual fields and give them weight
        in the order title -> title_slug -> content_text, each both
        case sensitiv & case insensitiv. We match those fields for
        the whole `query_str` as well as the individual parts and
        the parts slugified. Those checks are then also used as an
        overall filter, so only results containing those strings are
        looked at and returned.
        """
        query_str_slug = slugify(query_str).replace("-", " ")

        query = super().get_queryset()
        query = query.annotate(
            rank=SearchRank(F("search_vector"), SearchQuery(query_str)),
            rankmatch=Case(When(rank__gt=0.5, then=1), default=0),
        )

        lookups = {
            "title__contains": 10,
            "title__ilike": 9,
            "title_slug__contains": 8,
            "title_slug__ilike": 7,
        }
        if with_content:
            lookups["content_text__contains"] = 6
            lookups["content_text__ilike"] = 5

        q = Q()
        w = []
        for lookup, value in lookups.items():
            q |= Q(**{lookup: query_str})
            w += [When(**{lookup: query_str, "then": value})]
            w += [When(**{lookup: query_str_slug, "then": value - 1})]

        words = (query_str + query_str_slug).split()
        parts = set(words)
        if len(parts) > 1:
            for part in parts:
                for lookup, value in lookups.items():
                    q |= Q(**{lookup: part})
                    w += [When(**{lookup: part, "then": value - 4})]

        query = (
            query.filter(q)
            .annotate(contains=Case(*w, default=0))
            .order_by("-contains", "id")
        )

        query = query.order_by("-rankmatch", "-contains", "id")

        if content_types:
            query = query.filter(content_type__in=content_types)
        return query.values(
            "content_type", "object_id", "title", "content", "contains", "rankmatch"
        )


class SearchEntry(models.Model):
    """
    An entry in the search table pointing to a Django model instance
    """

    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE, null=True)
    object_id = models.PositiveIntegerField(null=True)
    content_object = GenericForeignKey()

    title = models.CharField(max_length=1024)
    title_slug = models.CharField(max_length=1024)

    content = models.JSONField()
    content_text = models.TextField(null=True)

    search_vector = SearchVectorField()

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
            GinIndex(
                name="search_sear_title_slug_gin",
                fields=["title_slug"],
                opclasses=["gin_trgm_ops"],
            ),
            GinIndex(fields=["search_vector"]),
        ]

    @classmethod
    def reindex_model_instance(cls, instance):
        content_type = ContentType.objects.get_for_model(instance)

        title = str(instance)
        title_slug = slugify(title).replace("-", " ")

        serialization = get_search_serialization_from_instance(instance)

        serialization_text = {k: v for k, v in serialization.items() if v}
        serialization_slugs = [
            slugify(sentence).split("-") for sentence in serialization_text.values()
        ]
        content_text = set(functools.reduce(operator.iconcat, serialization_slugs, []))

        defaults = {
            "title": title,
            "title_slug": title_slug,
            "content": serialization,
            "content_text": " ".join(sorted(content_text)),
        }
        s, c = cls.objects.update_or_create(
            content_type=content_type, object_id=instance.pk, defaults=defaults
        )
        s.search_vector = (
            SearchVector("title", weight="A")
            + SearchVector("title_slug", weight="B")
            + SearchVector("content_text", weight="C")
        )
        s.save()

    @classmethod
    def delete(cls, instance):
        content_type = ContentType.objects.get_for_model(instance)

        cls.objects.filter(content_type=content_type, object_id=instance.pk).delete()
