from typing import List, Union

from .api import FeedbackResponse
from .artefact import Artefact
from .document import Form, ParentDocument
from .enum import ClientEnv
from .label import Feedback, Prediction
from .page import BBox, ImageFormat, Page
from .projection import ProjectionRoot
from .target import Document, Target
from .upload import Metadata

SaverArgType = Union[List[Page], List[ProjectionRoot], Prediction, bytes]

__all__ = [
    "Artefact",
    "ClientEnv",
    "Feedback",
    "Prediction",
    "FeedbackResponse",
    "Form",
    "Metadata",
    "Target",
    "ParentDocument",
    "Document",
    "Page",
    "BBox",
    "ImageFormat",
    "ProjectionRoot",
    "SaverArgType",
]
