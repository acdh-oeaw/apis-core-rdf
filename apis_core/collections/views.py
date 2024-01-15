from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.contenttypes.models import ContentType
from django.views.generic.base import TemplateView
from django.shortcuts import redirect, get_object_or_404

from .models import SkosCollection, SkosCollectionContentObject


class ContentObjectMixin:
    """
    Setup the ContentType and the object used by a view, based on the
    `content_type_id` and the `object_id` arguments passed in the URL.
    """

    def setup(self, *args, **kwargs):
        super().setup(*args, **kwargs)
        self.content_type = get_object_or_404(ContentType, pk=kwargs["content_type_id"])
        self.object = get_object_or_404(
            self.content_type.model_class(), pk=kwargs["object_id"]
        )

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        context["content_type"] = self.content_type
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
            content_type=self.content_type,
            object_id=self.object.id,
        )
        if not self.created:
            scco.delete()
        if redirect_to := self.request.GET.get("to", False):
            return redirect(redirect_to)
        return super().get(*args, **kwargs)


class CollectionObjectParent(LoginRequiredMixin, ContentObjectMixin, TemplateView):
    """
    Change the requested CollectionObjects collection to point to the parent of the
    current collection.
    """

    template_name = "collections/collection_object_parent.html"

    def get_context_data(self, *args, **kwargs):
        collectionobject = get_object_or_404(
            SkosCollectionContentObject, pk=kwargs["collectionobject"]
        )
        if collectionobject.collection.parent:
            collectionobject.collection = collectionobject.collection.parent
            collectionobject.save()
        context = super().get_context_data(*args, **kwargs)
        context["collectionobject"] = collectionobject
        return context
