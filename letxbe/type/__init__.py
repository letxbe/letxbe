from typing import Union

from .api import FeedbackResponse
from .artefact import Artefact
from .document import Form, ParentDocument
from .enum import ClientEnv
from .label import Feedback
from .target import Target
from .upload import Metadata

Document = Union[Target, Artefact]

__all__ = [
    "Artefact",
    "ClientEnv",
    "Feedback",
    "FeedbackResponse",
    "Form",
    "Metadata",
    "Target",
    "ParentDocument",
]
