import django_filters

from .models import Uri


class UriListFilter(django_filters.FilterSet):
    uri = django_filters.CharFilter(lookup_expr="icontains")

    class Meta:
        model = Uri
        fields = ("uri",)
