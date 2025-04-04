from django import template
from django.contrib.contenttypes.models import ContentType

from apis_core.collections.models import SkosCollection, SkosCollectionContentObject

register = template.Library()


### templatetags for the APIS collections model ###


@register.inclusion_tag("collections/collection_toggle.html", takes_context=True)
def collection_toggle(context, obj, collection):
    """
    Provide a button to add or remove a connection between a
    collection and an object.
    """
    content_type = ContentType.objects.get_for_model(obj)
    context["content_type"] = content_type
    context["object"] = obj
    context["collection"] = collection
    context["exists"] = SkosCollectionContentObject.objects.filter(
        object_id=obj.id, content_type=content_type, collection=collection
    ).exists()
    return context


@register.inclusion_tag("collections/collection_toggle.html", takes_context=True)
def collection_toggle_by_id(context, obj, collectionid):
    """
    Wrapper templatetag to allow using `collection_toggle`
    with just the `id` of the collection.
    """
    collection = SkosCollection.objects.get(pk=collectionid)
    return collection_toggle(context, obj, collection)


@register.inclusion_tag(
    "collections/collection_object_collection.html", takes_context=True
)
def collection_object_collection(context, obj, skoscollectioncollectionobjects):
    """
    Provide a button to change the connection between an object and
    a collection to point to the collection the collection is in.
    """
    if len(skoscollectioncollectionobjects) > 1:
        context["error"] = (
            "Multiple collections found to toggle, please check `collection_object_collection`"
        )
    if len(skoscollectioncollectionobjects) == 1:
        collectionobject = skoscollectioncollectionobjects.first()
        context["parent"] = collectionobject.collection.parent_collection
        context["collectionobject"] = collectionobject
        context["content_type"] = ContentType.objects.get_for_model(obj)
        context["object"] = obj
    return context


@register.inclusion_tag(
    "collections/collection_object_collection.html", takes_context=True
)
def collection_object_collection_by_id(context, obj, *collection_ids):
    """
    Wrapper templatetag to allow using `collection_object_parent` with
    just the `ids` of collections.
    """
    content_type = ContentType.objects.get_for_model(obj)
    sccos = SkosCollectionContentObject.objects.filter(
        collection__in=collection_ids, content_type=content_type, object_id=obj.id
    )
    return collection_object_collection(context, obj, sccos)


@register.simple_tag(takes_context=True)
def collection_content_objects(context, obj, collectionids=None):
    content_type = ContentType.objects.get_for_model(obj)
    sccos = SkosCollectionContentObject.objects.filter(
        content_type=content_type, object_id=obj.id
    )
    if collectionids is not None:
        ids = collectionids.split(",")
        sccos = sccos.filter(collection__id__in=ids)
    return sccos


@register.inclusion_tag(
    "collections/collection_session_toggle.html", takes_context=True
)
def collection_session_toggle_by_id(context, collection_id):
    """
    Provide a checkbox to toggle if a session collection is active.
    The checkbox calls the CollectionSessionToggle view.
    """
    session_collections = context.request.session.get("session_collections", [])
    context["collection"] = SkosCollection.objects.get(pk=collection_id)
    context["enabled"] = collection_id in session_collections
    return context
