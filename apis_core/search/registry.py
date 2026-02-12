class SearchRegistry:
    def __init__(self):
        self._registry = {}  # Store model -> config

    def register(self, model, **options):
        """Register a model with optional configuration."""
        self._registry[model] = options

    def is_registered(self, model):
        """Check if a model is registered."""
        return model in self._registry

    def get_config(self, model):
        """Get configuration for a registered model."""
        return self._registry.get(model)

    def unregister(self, model):
        """Unregister a model."""
        if model in self._registry:
            del self._registry[model]

    def get_registered_models(self):
        """Return all registered models."""
        return self._registry.keys()


registry = SearchRegistry()


# registry.py (add this method)
def register(model=None, **options):
    """Decorator to register a model."""

    def _register(model):
        registry.register(model, **options)
        return model

    if model:
        return _register(model)
    return _register
