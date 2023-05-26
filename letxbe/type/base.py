import re
from typing import Any, Union

from pydantic import BaseModel, StrictBool, StrictFloat, StrictInt, StrictStr, validator

ValueType = Union[StrictInt, StrictBool, StrictFloat, StrictStr]


def assert_type_and_value_equality(value_1: ValueType, value_2: ValueType) -> None:
    """Assert two values are equal and of the same type if one of them is boolean.

    Args:
        value_1 (ValueType):
        value_2 (ValueType):
    """
    if (
        isinstance(value_1, bool)
        and not isinstance(value_2, bool)
        or not isinstance(value_1, bool)
        and isinstance(value_2, bool)
    ):
        raise AssertionError(
            f"Values do not share the same type: '{value_1}', '{value_2}'."
        )
    assert value_1 == value_2


slug_regex = re.compile(r"[a-zA-Z\-0-9]+")
low_key_regex = re.compile(r"[a-zA-Z\_0-9]+")


class SlugMixin(BaseModel):
    """A resource that can be uniquely identified with a single `slug`.

    Attributes:
        slug (str): Unique identifier that can be used in a URL.
    """

    slug: str

    @validator("slug")
    def enforce_slug_regex_on_slugs(cls: Any, value: str) -> str:
        """Validate the format of `SlugMixin.slug`.

        Args:
            value (str): The value of the slug.

        Returns:
            str: The value of the slug if supported.

        raises:
            ValueError: The value of the slug is not supported.
        """

        if slug_regex.fullmatch(value) is None:
            raise ValueError(
                f"Error with slug '{value}': must be compatible with base.slug_regex."
            )
        return value


class CreatedMixin(BaseModel):
    """A resource that can be created.

    Attributes:
        created_at (int): Timestamp in milliseconds corresponding to the creation of
            the object. Set to 0 at default.
    """

    created_at: int = 0
