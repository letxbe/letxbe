from typing import Dict

from pydantic import BaseModel


class Task(BaseModel):
    """
    Define a task to be run for a service.

    Args:
        slug (str): A unique identifier for the task.
        order (Dict): Parameters for the task.

    """

    slug: str
    order: Dict
