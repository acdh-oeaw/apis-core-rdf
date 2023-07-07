from django import template
from django.db.models import Q
from apis_core.apis_relations.models import Triple
from apis_core.apis_relations.tables import TripleTable
from apis_core.apis_relations.forms import TripleForm

register = template.Library()

# For django-tables2 to work we have to pass the request, see https://github.com/jieter/django-tables2/issues/321
# We could also use `uses_context`, but that breaks crispy forms https://github.com/django-crispy-forms/django-crispy-forms/issues/853
@register.inclusion_tag("apis_relations/partials/triple_from_instance_to_entity.html")
def triple_from_instance_to_entity_contenttype(
    request, instance, entity_contenttype, *args, **kwargs
):
    queryset = Triple.objects.filter(
        (Q(subj=instance) & Q(obj__self_contenttype=entity_contenttype))
        | (Q(obj=instance) & Q(subj__self_contenttype=entity_contenttype))
    )
    formprefix = f"{entity_contenttype.app_label}.{entity_contenttype.model}"
    return {
        "request": request,
        "instance": instance,
        "entity_contenttype": entity_contenttype,
        "table": TripleTable(queryset),
        "form": TripleForm(instance, entity_contenttype, prefix=formprefix),
    }
