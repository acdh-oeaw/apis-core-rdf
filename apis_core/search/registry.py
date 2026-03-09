class SearchRegistry:
    def __init__(self):
        self._registry = {}  # Store model -> config

    def register(self, model, **options):
        self._registry[model] = options

    def is_registered(self, model):
        return model in self._registry

    def get_registered_models(self):
        return self._registry.keys()


registry = SearchRegistry()


def register(model=None, **options):
    """Decorator to register a model."""

    def _register(model):
        registry.register(model, **options)
        return model

    if model:
        return _register(model)
    return _register
