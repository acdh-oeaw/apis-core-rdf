Working with collections
========================

APIS comes with models to make working with collections easier. These can be
used to build vocabularies or a tagging solution or even a workflow solution.
To use it, you have to add `apis_core.collections` to your `INSTALLED_APPS`.

The `collections` module consists of the two models
:py:class:`apis_core.collections.models.SkosCollection` and
:py:class:`apis_core.collections.models.SkosCollectionContentObject`. The former
is the class for the collection vocabularies, whereas the latter lets you
connect specific collections with any content instance, using generic
relations. `SkosCollection` objects can have another `SkosCollection` as a
parent, which lets you create hierarchies.

You can create your collections in the `admin` interface or using the `generic` app.

If you want to use collections to provide choices for a form, you can either
use a :py:class:`django.models.ForeignKey` or use use a
:py:class:`django.models.CharField` and you customize the model form to use the
collection as choices for this field. Both approaches have pros and cons.

There are a couple of templatetags that make working with collection easier, they
all reside in the :py:mod:`apis_core.collections.templatetags.apis_collections`
templatetag library. If you use them, you have to include
:py:mod:`apis_core.collections.urls` into your urls.py, for example like this:

.. code-block:: python

   urlpatterns = [
       ...
       path("apis/collections/", include("apis_core.collections.urls")),
       ...


The templatetags are:

* :py:func:`apis_core.collections.templatetags.apis_collections.collection_toggle`
  and
  :py:func:`apis_core.collections.templatetags.apis_collections.collection_toggle_by_id`

This templatetag takes the instance of an object and a collection (or, in the
case of `_by_id` the id of a collection) and lets the user create and remove
the connection between this instance and the collection.

* :py:func:`apis_core.collections.templatetags.apis_collections.collection_children_toggle`
  and
  :py:func:`apis_core.collections.templatetags.apis_collections.collection_children_toggle_by_id`

This is a helper templatetag that creates toggle buttons for all the child
collections of a collection. This way you can use one collections a parent for
a couple of tags and simply add the parent of a new tag collection to the
parent collection and it automatically shows up in this toggle button list.

* :py:func:`apis_core.collections.templatetags.apis_collections.collection_object_parent`
  and
  :py:func:`apis_core.collections.templatetags.apis_collections.collection_object_parent_by_id`

This templatetag provides a button to change the connection from an instance to
a collection to point to the collections parent. This is useful if you want to
implement a workflow (i.e. three collections: `done` as the root one, `in
process` with `done` as parent and `todo` with `in process` as parent - the
user can then on the click of a button change an the collection an instance is
connected to)
