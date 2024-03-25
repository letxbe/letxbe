import json
import random
import string
from typing import cast

from pydantic import BaseModel

ALPHABET = string.ascii_lowercase + string.digits


def pydantic_model_to_json(model: BaseModel) -> dict:
    """Convert any model to a json that can be used as a query parameter for arangodb.

    It is however preferable to create requests that do not take json as a query
    parameter but go explicitly inside the structure.

    When using .dict(), some types including enums seem to not be exported as strings.

    Args:
        model (BaseModel): Pydantic model to convert.

    Returns:
        Dictionary representation of a model.
    """
    return cast(dict, json.loads(model.json()))


def generate_short_unique_id() -> str:
    return "".join(random.choices(ALPHABET, k=12))
