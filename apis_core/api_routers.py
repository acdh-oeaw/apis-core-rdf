from functools import reduce

try:
    from apis_ontology.models import *
except ImportError:
    pass
from apis_core.apis_metainfo.models import *

# from django.contrib.contenttypes.models import ContentType
from django.urls import reverse
from django.conf import settings
from rest_framework import pagination, serializers, viewsets
from rest_framework import renderers
from rest_framework.response import Response

from drf_spectacular.utils import (
    extend_schema,
    extend_schema_field,
)
from drf_spectacular.types import OpenApiTypes
from django_filters import rest_framework as filters
from apis_core.apis_entities.models import TempEntityClass
from .api_renderers import NetJsonRenderer
from .apis_relations.models import Triple, Property
from apis_core.utils import caching
from apis_core.core.mixins import ListViewObjectFilterMixin

try:
    MAX_AGE = settings.MAX_AGE
except AttributeError:
    MAX_AGE = 0


def deep_get(dictionary, keys, default=None):
    return reduce(
        lambda d, key: d.get(key, default) if isinstance(d, dict) else default,
        keys.split("."),
        dictionary,
    )


def create_query_parameters(entity):
    print(entity)
    for f in entity._meta.fields:
        print(f.name, f.__class__.__name__)


class CustomPagination(pagination.LimitOffsetPagination):
    def get_paginated_response(self, data):
        return Response(
            {
                "next": self.get_next_link(),
                "previous": self.get_previous_link(),
                "count": self.count,
                "limit": self.limit,
                "offset": self.offset,
                "results": data,
            }
        )


class ApisBaseSerializer(serializers.ModelSerializer):
    id = serializers.ReadOnlyField()
    label = serializers.SerializerMethodField(method_name="add_label")
    url = serializers.SerializerMethodField(method_name="add_uri")

    @extend_schema_field(OpenApiTypes.INT)
    def add_id(self, obj):
        return obj.pk

    @extend_schema_field(OpenApiTypes.STR)
    def add_label(self, obj):
        return str(obj)

    @extend_schema_field(OpenApiTypes.URI)
    def add_uri(self, obj):
        return self.context["view"].request.build_absolute_uri(
            reverse(
                "apis:apis_api:{}-detail".format(obj.__class__.__name__.lower()),
                kwargs={"pk": obj.pk},
            )
        )

    class Meta:
        model = TempEntityClass
        fields = ["id", "label", "url"]


class EntitySerializer(ApisBaseSerializer):
    type = serializers.SerializerMethodField(method_name="add_type")

    def add_type(self, instance):
        return instance.__class__.__name__

    class Meta(ApisBaseSerializer.Meta):
        fields = ApisBaseSerializer.Meta.fields + ["type"]


class LabelSerializer(ApisBaseSerializer):
    parent_id = serializers.PrimaryKeyRelatedField(
        many=False, source="parent_class_id", read_only=True
    )

    @extend_schema_field(OpenApiTypes.INT)
    def add_parent_id(self, obj):
        return obj.parent_class_id

    class Meta(ApisBaseSerializer.Meta):
        fields = ApisBaseSerializer.Meta.fields + [
            "parent_id",
        ]


class RelatedTripleSerializer(ApisBaseSerializer):
    relation_type = serializers.SerializerMethodField(
        method_name="add_related_property"
    )
    related_entity = serializers.SerializerMethodField(method_name="add_related_entity")

    class Meta:
        model = Triple
        fields = ["id", "url", "relation_type", "related_entity"]

    def __init__(self, *args, **kwargs):
        self._pk_instance = kwargs.pop("pk_instance")
        super(RelatedTripleSerializer, self).__init__(*args, **kwargs)

    def add_related_property(self, triple):
        if triple.subj.pk == self._pk_instance:

            class RelatedPropertySerializer(ApisBaseSerializer):
                label = serializers.CharField(source="name_forward")

                class Meta:
                    model = Property
                    fields = ["id", "label", "url"]

        elif triple.obj.pk == self._pk_instance:

            class RelatedPropertySerializer(ApisBaseSerializer):
                label = serializers.CharField(source="name_reverse")

                class Meta:
                    model = Property
                    fields = ["id", "label", "url"]

        else:
            raise Exception(
                "Did not find entity in triple where it is supposed to be. Something must be wrong with the code."
            )
        return RelatedPropertySerializer(triple.prop, context=self.context).data

    def add_related_entity(self, triple):
        if triple.subj.pk == self._pk_instance:
            return EntitySerializer(triple.obj, context=self.context).data
        elif triple.obj.pk == self._pk_instance:
            return EntitySerializer(triple.subj, context=self.context).data
        else:
            raise Exception(
                "Did not find entity in triple where it is supposed to be. Something must be wrong with the code."
            )


def generic_serializer_creation_factory():
    lst_cont = caching.get_all_contenttype_classes()
    not_allowed_filter_fields = [
        "useradded",
        "parent_class",
        "entity",
        "autofield",
    ]
    for cont in lst_cont:
        prefetch_rel = []
        select_related = []
        test_search = getattr(settings, cont.__module__.split(".")[1].upper(), False)
        entity_str = str(cont.__name__).replace(" ", "")
        entity = cont
        app_label = cont.__module__.split(".")[1].lower()
        exclude_lst = []
        if app_label == "apis_entities":
            exclude_lst = deep_get(test_search, "{}.api_exclude".format(entity_str), [])
        else:
            set_prem = getattr(settings, cont.__module__.split(".")[1].upper(), {})
            exclude_lst = deep_get(set_prem, "exclude", [])
            exclude_lst.extend(deep_get(set_prem, "{}.exclude".format(entity_str), []))
        entity_field_name_list = []
        for x in entity._meta.get_fields():
            entity_field_name_list.append(x.name)
        exclude_lst_fin = []
        for x in exclude_lst:
            if x in entity_field_name_list:
                exclude_lst_fin.append(x)
        for f in entity._meta.get_fields():
            if f.__class__.__name__ == "ManyToManyField":
                prefetch_rel.append(f.name)
            elif f.__class__.__name__ == "ForeignKey":
                select_related.append(f.name)

        class TemplateSerializer(serializers.HyperlinkedModelSerializer):

            id = serializers.ReadOnlyField()
            if getattr(settings, "APIS_API_ID_WRITABLE", False):
                id = serializers.IntegerField()
            url = serializers.HyperlinkedIdentityField(
                view_name=f"apis:apis_api:{entity_str.lower()}-detail"
            )
            _entity = entity
            _exclude_lst = exclude_lst_fin
            _app_label = app_label

            class Meta:

                model = entity
                exclude = exclude_lst_fin

            def add_labels(self, obj):
                return {"id": obj.pk, "label": str(obj)}

            def __init__(self, *args, **kwargs):
                super().__init__(*args, **kwargs)
                for f in self._entity._meta.get_fields():
                    if getattr(settings, "APIS_API_EXCLUDE_SETS", False) and str(
                        f.name
                    ).endswith("_set"):
                        if f.name in self.fields.keys():
                            self.fields.pop(f.name)
                        continue
                    ck_many = f.__class__.__name__ == "ManyToManyField"
                    if f.name in self._exclude_lst:
                        continue
                    elif f.__class__.__name__ in [
                        "ManyToManyField",
                        "ForeignKey",
                        "InheritanceForeignKey",
                    ]:
                        self.fields[f.name] = ApisBaseSerializer(
                            many=ck_many, read_only=True
                        )
                    elif f.__class__.__name__ in ["ManyToManyField", "ForeignKey"]:
                        self.fields[f.name] = LabelSerializer(
                            many=ck_many, read_only=True
                        )

        TemplateSerializer.__name__ = (
            TemplateSerializer.__qualname__
        ) = f"{entity_str.title().replace(' ', '')}Serializer"

        class TemplateSerializerRetrieve(TemplateSerializer):
            def __init__(self, *args, **kwargs):
                super().__init__(*args, **kwargs)
                for f in self._entity._meta.get_fields():
                    if getattr(settings, "APIS_API_EXCLUDE_SETS", False) and str(
                        f.name
                    ).endswith("_set"):
                        if f.name in self.fields.keys():
                            self.fields.pop(f.name)
                        continue
                    ck_many = f.__class__.__name__ == "ManyToManyField"
                    if f.name in self._exclude_lst:
                        continue
                    elif f.__class__.__name__ in [
                        "ManyToManyField",
                        "ForeignKey",
                    ]:
                        self.fields[f.name] = ApisBaseSerializer(
                            many=ck_many, read_only=True
                        )
                    elif f.__class__.__name__ in ["ManyToManyField", "ForeignKey"]:
                        self.fields[f.name] = LabelSerializer(
                            many=ck_many, read_only=True
                        )
                if len(args) > 0:
                    entity = args[0]
                    if hasattr(entity, "triple_set_from_subj") or hasattr(
                        entity, "triple_set_from_obj"
                    ):
                        self.fields["relations"] = RelatedTripleSerializer(
                            read_only=True,
                            source="get_triples",
                            many=True,
                            pk_instance=entity.pk,
                        )

        TemplateSerializerRetrieve.__name__ = (
            TemplateSerializerRetrieve.__qualname__
        ) = f"{entity_str.title().replace(' ', '')}DetailSerializer"

        allowed_fields_filter = {
            "IntegerField": ["in", "range", "exact"],
            "CharField": ["exact", "icontains", "iregex", "isnull"],
            "DateField": ["year", "lt", "gt", "year__lt", "year__gt", "exact"],
            "PositiveIntegerField": ["in", "range", "exact"],
            "AutoField": ["in", "exact"],
        }
        filterset_dict = {}
        filter_fields = {}

        for field in entity._meta.fields + entity._meta.many_to_many:
            if getattr(settings, "APIS_API_EXCLUDE_SETS", False) and "_set" in str(
                field.name.lower()
            ):
                continue
            if (
                field.name.lower() in not_allowed_filter_fields
                or field.name == "tempentityclass_ptr"
            ):
                continue
            elif field.__class__.__name__ in ["ForeignKey", "ManyToManyField"]:
                filter_fields[field.name] = ["exact"]
                if field.__class__.__name__ == "ForeignKey":
                    filter_fields[field.name].append("in")
                for f2 in field.related_model._meta.fields:
                    if f2.__class__.__name__ in [
                        "CharField",
                        "DateField",
                        "IntegerField",
                        "AutoField",
                    ]:
                        filter_fields[
                            f"{field.name}__{f2.name}"
                        ] = allowed_fields_filter[f2.__class__.__name__]
                continue
            if field.__class__.__name__ in allowed_fields_filter.keys():
                filter_fields[field.name] = allowed_fields_filter[
                    field.__class__.__name__
                ]
            else:
                filter_fields[field.name] = ["exact"]
        additional_filters = getattr(settings, "APIS_API_ADDITIONAL_FILTERS", False)
        if additional_filters:
            if entity_str in additional_filters.keys():
                for f1 in additional_filters[entity_str]:
                    if f1[0] not in filter_fields.keys():
                        filter_fields[f1[0]] = f1[1]

        class MetaFilter(object):

            model = entity
            fields = filter_fields

        filterset_dict["Meta"] = MetaFilter

        class TemplateViewSet(ListViewObjectFilterMixin, viewsets.ModelViewSet):

            _select_related = select_related
            _prefetch_rel = prefetch_rel
            pagination_class = CustomPagination
            model = entity
            # filter_backends = (DjangoFilterbackendSpectacular,)
            filter_backends = (filters.DjangoFilterBackend,)
            filterset_fields = filter_fields
            depth = 2
            renderer_classes = (
                renderers.JSONRenderer,
                renderers.BrowsableAPIRenderer,
                NetJsonRenderer,
            )
            _serializer_class = TemplateSerializer
            _serializer_class_retrieve = TemplateSerializerRetrieve

            def get_serializer_class(self, *arg, **kwargs):
                if self.action == "list":
                    return self._serializer_class
                else:
                    return self._serializer_class_retrieve

            def get_serializer_context(self):
                context = super(self.__class__, self).get_serializer_context()
                if self.action == "retrieve" and self.model.__name__.lower() == "text":
                    cont = {}
                    cont["highlight"] = self.request.query_params.get("highlight", None)
                    cont["ann_proj_pk"] = self.request.query_params.get(
                        "ann_proj_pk", None
                    )
                    cont["types"] = self.request.query_params.get("types", None)
                    cont["users_show"] = self.request.query_params.get(
                        "users_show", None
                    )
                    cont["inline_annotations"] = self.request.query_params.get(
                        "inline_annotations", True
                    )
                    context.update(cont)
                return context

            def get_queryset(self):
                if "apis_relations" in str(self.model):
                    qs = self.model.objects.filter_for_user()
                else:
                    qs = self.model.objects.all()
                if len(self._prefetch_rel) > 0:
                    qs = qs.prefetch_related(*self._prefetch_rel)
                if len(self._select_related) > 0:
                    qs = qs.select_related(*self._select_related)
                return self.filter_queryset(qs)

            @extend_schema(responses=TemplateSerializer(many=True))
            def list_viewset(self, request):
                res = super(self.__class__, self).list(request)
                return res

            def dispatch(self, request, *args, **kwargs):
                return super(self.__class__, self).dispatch(request, *args, **kwargs)

        TemplateViewSet.__name__ = (
            TemplateViewSet.__qualname__
        ) = f"Generic{entity_str.title().replace(' ', '')}ViewSet"

        serializers_dict[TemplateSerializer] = TemplateSerializer
        views[f"{entity_str.lower().replace(' ', '')}"] = TemplateViewSet


# TODO: What is this dict 'serializers_dict' used for?
# I don't find any usage anywhere else and above it gets filled with classes where they are key and value at the same time,
# which doesn't make sense
serializers_dict = dict()
views = dict()
generic_serializer_creation_factory()
