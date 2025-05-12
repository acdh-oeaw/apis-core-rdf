from collections import ChainMap


class TypeCheckerMetaClass(type):
    """
    This metaclass checks if all the attributes adhere to their type annotations.
    Child classes have to adhere to their parent type annotations, unless they
    overload the type annotations.
    """

    def __new__(cls, name, bases, attrs):
        annotations = attrs.get("__annotations__", {})
        for base in bases:
            annotations.update(
                ChainMap(
                    *(
                        c.__annotations__
                        for c in base.__mro__
                        if "__annotations__" in c.__dict__
                    )
                )
            )
        for key, val in annotations.items():
            if key in attrs and type(attrs[key]) is not val:
                raise ValueError(f"{name}.{key} should be {val}")
        return super().__new__(cls, name, bases, attrs)
