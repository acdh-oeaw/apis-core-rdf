from django.core.serializers.json import Serializer


class SearchSerializer(Serializer):
    """
    This serializer is based on the default JSON serializer shipped in Django core.
    The only change is, that is serializes m2m fields as list of string representations
    instead of list of ids
    """

    def handle_m2m_field(self, obj, field):
        """This is copied from the parent class, only the last line was changed"""
        if field.remote_field.through._meta.auto_created:

            def queryset_iterator(obj, field):
                query_set = getattr(obj, field.name).select_related(None).only("pk")
                chunk_size = 2000 if query_set._prefetch_related_lookups else None
                return query_set.iterator(chunk_size=chunk_size)

            m2m_iter = getattr(obj, "_prefetched_objects_cache", {}).get(
                field.name,
                queryset_iterator(obj, field),
            )
            self._current[field.name] = ", ".join(
                [str(related) for related in m2m_iter]
            )
