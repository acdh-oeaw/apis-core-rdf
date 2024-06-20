Configuration
=============


``APIS_BASE_URL`` and :class:`apis_core.apis_entities.api_views.GetEntityGeneric`
------------------------------------------------------------------------------

When you create an instance of an Entity a signal
:py:func:`apis_core.apis_entities.models.create_default_uri` is triggered that
tries to generate a canonical URI for the entity. The signal can be disabled by
setting the ``CREATE_DEFAULT_URI`` setting to ``False``.
If the signal runs, it creates the canoncical URI from two parts. The first part
comes from the ``APIS_BASE_URI`` setting. The second part comes from the reverse
route of ``GetEntityGenericRoot`` if that exists. If not, it uses the
the reverse route of ``apis_core:GetEntityGeneric``, which is defined in
:py:mod:`apis_core.urls` and defaults to ``/entity/{pk}``.
