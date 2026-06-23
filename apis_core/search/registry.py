class SearchRegistry:
    """A registry storing models and their configs for search"""

    def __init__(self):
        self._registry = {}  # Store model -> config

    def is_registered(self, model):
        return model in self._registry

    def get_registered_models(self):
        return self._registry.keys()

    def get_options(self, model):
        return self._registry.get(model, {})

    def register(self, model=None, **options):
        """Decorator to register a model."""

        def _register(model):
            self._registry[model] = options
            return model

        if model:
            return _register(model)
        return _register


search = SearchRegistry()
