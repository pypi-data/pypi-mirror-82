import typing

__all__ = (
    "LimeUoWException",
    "DuplicateResourceNames",
    "InvalidResource",
    "MissingResourceError",
    "OutsideTransactionError",
    "RollbackError",
)


class LimeUoWException(Exception):
    """Base class for exceptions arising from the lime-uow package"""

    def __init__(self, message: str, /):
        self.message = message
        super().__init__(message)


class DuplicateResourceNames(LimeUoWException):
    def __init__(self, duplicates: typing.Mapping[str, int], /):
        self.duplicates = duplicates

        examples = ", ".join(
            f"{name} = {ct}" for name, ct in sorted(duplicates.items())
        )
        msg = f"Resource names must be unique, but found the following duplicates: {examples}."
        super().__init__(msg)


class InvalidResource(LimeUoWException):
    def __init__(self, message: str, /):
        super().__init__(message)


class MissingResourceError(LimeUoWException):
    def __init__(
        self, *, resource_name: str, available_resources: typing.Iterable[str]
    ):
        self.resource_name = resource_name
        msg = (
            f"Could not locate a resource named {resource_name!r}.  "
            f"Available resources include the following: {', '.join(available_resources)}."
        )
        super().__init__(msg)


class NoCommonAncestor(LimeUoWException):
    def __init__(self, message: str, /):
        super().__init__(message)


class OutsideTransactionError(LimeUoWException):
    def __init__(self):
        super().__init__(
            "Attempted to access a UnitOfWork resource outside a with block."
        )


class RollbackError(LimeUoWException):
    def __init__(self, message: str, /):
        super().__init__(message)
