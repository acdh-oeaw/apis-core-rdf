from drf_spectacular.openapi import AutoSchema


class GenericAutoSchema(AutoSchema):
    """
    Add an option to the default drf_spectacular schema that
    allows to set the tags of a route via the model.
    """

    def get_tags(self) -> list[str]:
        model = getattr(self.view, "model", None)
        if hasattr(model, "get_openapi_tags"):
            return model.get_openapi_tags()
        return super().get_tags()
