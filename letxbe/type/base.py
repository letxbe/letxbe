import re
from typing import Any, Union

from pydantic import BaseModel, StrictBool, StrictFloat, StrictInt, StrictStr, validator

ValueType = Union[StrictInt, StrictBool, StrictFloat, StrictStr]


def assert_type_and_value_equality(value_1: ValueType, value_2: ValueType) -> None:
    """
    Ensure two values are equal and of the same type.
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
key_regex = re.compile(r"[a-zA-Z\-\_0-9]+")
low_key_regex = re.compile(r"[a-zA-Z\_0-9]+")


class Web(BaseModel):
    """
    A resource that can be uniquely identified with a single `slug`.

    slug: a unique identifier that can be used in a URL
    """

    slug: str

    @validator("slug")
    def enforce_slug_regex_on_slugs(cls: Any, value: str) -> str:
        """
        Validate the format of `Web.slug`.

        raises:
            ValueError: the value of the slug is not supported.
        """

        if slug_regex.fullmatch(value) is None:
            raise ValueError(
                f"Error with slug '{value}': must be compatible with base.slug_regex."
            )
        return value


class Dated(BaseModel):
    """
    A resource that can be created and updated.

    created_at: timestamp in milliseconds corresponding to the creation of the object.
    updated_at: timestamp in milliseconds corresponding to the moment the last edit was
        made on the object.
    """

    created_at: int = 0
    updated_at: int = 0


class Vertex(Web, Dated):
    """
    A resource stored in database.
    """
