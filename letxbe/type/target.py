"""

A `Target` is a `Document` that can be processed to generate and store a `Prediction` or `Feedback`.

"""
from typing import Literal, Optional, Union

from pydantic import BaseModel

from .artefact import Artefact, ArtefactConnectionMixin
from .document import DocumentMixin, StatusMixin, WithParentMixin
from .label import Current, Feedback, Prediction


class TargetMixin(BaseModel):
    """Information specific to a `Target`_.

    Attributes:
        role (Literal): equal to `None`, as opposed to `Artefact`_.
        prediction (Prediction): predictions made on the target.
        feedback (Feedback or None): contains aggregated confirmations, deletions or
            modifications of ``prediction``.
        current (Current): combines ``prediction`` and ``feedback`` to give the current
            prediction values.
    """

    role: Literal[None] = None
    prediction: Prediction = Prediction()
    feedback: Optional[Feedback] = None
    current: Current = Current()


class Target(
    DocumentMixin, TargetMixin, WithParentMixin, StatusMixin, ArtefactConnectionMixin
):
    """Document sent to letxbe to get predictions."""


Document = Union[Target, Artefact]
