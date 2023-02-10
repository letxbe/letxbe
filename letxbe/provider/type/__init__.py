from typing import List, Union

from .enum import DownloadResource, LogStatus, ServiceUrl
from .page import Page
from .prediction import Feedback, LabelFeedback, LabelPrediction, Prediction
from .projection import ProjectionRoot
from .task import Task

SaverArgType = Union[
    List[Page],
    List[ProjectionRoot],
    Prediction,
]

__all__ = [
    "ServiceUrl",
    "DownloadResource",
    "Task",
    "LogStatus",
    "ProjectionRoot",
    "Page",
    "Prediction",
    "Feedback",
    "LabelPrediction",
    "LabelFeedback",
    "SaverArgType",
]
