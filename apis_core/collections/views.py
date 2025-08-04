from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.contenttypes.models import ContentType
from django.shortcuts import get_object_or_404, redirect
from django.views.generic.base import TemplateView

from .models import SkosCollection, SkosCollectionContentObject


class ContentObjectMixin:
    """
    Setup the ContentType and the object used by a view, based on the
    `content_type_id` and the `object_id` arguments passed in the URL.
    """

    def setup(self, *args, **kwargs):
        super().setup(*args, **kwargs)
        self.obj_content_type = get_object_or_404(
            ContentType, pk=kwargs["content_type_id"]
        )
        self.object = get_object_or_404(
            self.obj_content_type.model_class(), pk=kwargs["object_id"]
        )

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        context["content_type"] = self.obj_content_type
        context["object"] = self.object
        return context


class CollectionToggle(LoginRequiredMixin, ContentObjectMixin, TemplateView):
    """
    Toggle a collection - if a CollectionObject connecting the requested object
    and collection does not exist, then create it. If it does exist, delete it.
    """

    template_name = "collections/collection_toggle.html"

    def setup(self, *args, **kwargs):
        super().setup(*args, **kwargs)
        self.collection = get_object_or_404(SkosCollection, pk=kwargs["collection"])

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        context["exists"] = self.created
        context["collection"] = self.collection
        return context

    def get(self, *args, **kwargs):
        scco, self.created = SkosCollectionContentObject.objects.get_or_create(
            collection=self.collection,
            content_type=self.obj_content_type,
            object_id=self.object.id,
        )
        if not self.created:
            scco.delete()
        if redirect_to := self.request.GET.get("to", False):
            return redirect(redirect_to)
        return super().get(*args, **kwargs)


class CollectionObjectCollection(LoginRequiredMixin, ContentObjectMixin, TemplateView):
    """
    Change the requested CollectionObjects collection to point to the collection the
    current collection is in.
    """

    template_name = "collections/collection_object_collection.html"

    def get_context_data(self, *args, **kwargs):
        collectionobject = get_object_or_404(
            SkosCollectionContentObject, pk=kwargs["collectionobject"]
        )
        parent = collectionobject.collection.parent_collection
        collectionobject.collection = parent
        collectionobject.save()
        context = super().get_context_data(*args, **kwargs)
        context["collectionobject"] = collectionobject
        return context


class CollectionSessionToggle(LoginRequiredMixin, TemplateView):
    """
    Toggle the existence of an SkosCollection in the `session_collections`
    session variable.
    This can be used in combination with the
    `collections.signals.add_to_session_collection` signal, to add objects
    to a collection if the collections id is listed in the session variable.
    The equivalent templateatag that calls this view is
    `collections.templatetags.collections.collection_session_toggle_by_id`
    """

    template_name = "collections/collection_session_toggle.html"

    def get_context_data(self, *args, **kwargs):
        ctx = super().get_context_data(*args, **kwargs)
        ctx["collection"] = self.skoscollection
        ctx["enabled"] = self.skoscollection.id in self.session_collections
        return ctx

    def get(self, *args, **kwargs):
        self.skoscollection = get_object_or_404(
            SkosCollection, pk=kwargs["skoscollection"]
        )
        self.session_collections = set(
            self.request.session.get("session_collections", [])
        )
        self.session_collections ^= {self.skoscollection.id}
        self.request.session["session_collections"] = list(self.session_collections)
        if redirect_to := self.request.GET.get("to", False):
            return redirect(redirect_to)
        return super().get(*args, **kwargs)
