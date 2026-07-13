from typing import Optional, Union

from django.utils.functional import Promise
from pydantic import BaseModel, ConfigDict, ValidationError


class ValidationModel(BaseModel):
    """
    A pydantic `BaseModel` that provides a class method to
    turn pydantic validation errors into strings, usable by
    Django to pass on to an `Error` for example.
    """

    @classmethod
    def validation_errors_to_error_messages(cls, validate_cls):
        errors = []
        try:
            cls.model_validate(validate_cls(), from_attributes=True)
        except ValidationError as e:
            for error in e.errors():
                for loc in error["loc"]:
                    errors.append(f"Config.{loc} {error['msg']}")
        return errors


class ConfigModel(ValidationModel):
    """
    Pydantic based valdiation model for the config class used
    in the `GenericModel`
    """

    model_config = ConfigDict(arbitrary_types_allowed=True)
    overview_section: Optional[Union[str, Promise]] = None
