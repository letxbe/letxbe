from typing import List, Union

from letxbe.type import Prediction

from .enum import DownloadResource, LogStatus, ServiceUrl, UploadResource
from .page import Page
from .projection import ProjectionRoot
from .task import Task

SaverArgType = Union[List[Page], List[ProjectionRoot], Prediction, bytes]

__all__ = [
    "ServiceUrl",
    "DownloadResource",
    "Task",
    "LogStatus",
    "ProjectionRoot",
    "Page",
    "SaverArgType",
    "UploadResource",
]
