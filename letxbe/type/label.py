import uuid
from typing import Dict, List, Optional, Union

from pydantic import BaseModel, Field

from .base import ValueType
from .enum import FeedbackVote
from .image import BBox

FEEDBACK_M2M_IDENTIFIER = "M2M"


class ClueMixin(BaseModel):
    """
    Define shared information between all clue formats.

    Attributes:
        role (str or None):  Role of (or reference to) the document that contains the
            source or the clue. If the clue comes from its attached document, then
            the value must be `None`. Else the value must be a reference to the
            artefact containing the clue (see artefacts keys in ``ArtefactConnectionMixin``).
        value (str): Clue value.
    """

    value: str = ""
    role: Optional[str]


class BBoxMixin(BaseModel):
    """
    Normalized coordinates of a bounding box in an image.

    Attributes:
        bbox (BBox): Bounding box (see type.image.BBox).
    """

    bbox: BBox


class PageClue(ClueMixin):
    """
    Point to a page in a document.

    Attributes:
        page_idx (int): Page index of a page in an original document.

    Remarks:
        If a document is a split version of an original one, `page_idx` is the
        page index of the page in the original document.
    """

    page_idx: int


class WordClue(PageClue):
    """
    Coordinates of a word in a ``Page`` object.

    Attributes:
        line_idx (int): Line index.
        word_idx (int): Word index.
        bbox (BBox or None): Normalized coordinates of a bounding box in an image.
            See type.image.BBox.
    """

    line_idx: int
    word_idx: int
    bbox: Optional[BBox] = None


class BBoxInPageClue(PageClue, BBoxMixin):
    """
    Point to a bounding box in a page of a document.
    """


class ProjectionClue(ClueMixin):
    """
    Contains information to extract a `ProjectionField` from a Document.

    Attributes:
        pkey (str): Key pointing to a list of `ProjectionRoot`
        xid (str): xid of the ProjectionRoot
        projection_entry (str): See `__ProjectionBase.projection_entry`
            # TODO rename this to `projection_path`

    Examples:
      - (without recursive structure) document.projection[pkey]
          - filter projection_root_list by `xid`
          - output projection_root.result[projection_entry]
      - (with recursive structure) # TODO add example
    """

    pkey: str
    xid: str
    projection_entry: str
    token_idx: Optional[int] = 0
    length: Optional[int] = 0


ClueType = Union[ProjectionClue, WordClue, BBoxInPageClue, PageClue]
"""Types of clues used in labels. See ``ProjectionClue``, ``BBoxInPageClue``,
``WordClue``, ``PageClue`` and ``Label`` for mor information."""


class ChildConnection(BaseModel):
    """
    Attributes:
        atms_slug (str):
        doc_slug (str):
    """

    atms_slug: str
    doc_slug: str


class Label(BaseModel):
    """
    Information produced about a `Target` and its connected `Artefact` documents.

    Attributes:
        lid (str): Unique identifier for the label.
        value (ValueType or None): Value of label. There can be only one Label with
            the same `value` in a `multiple prediction field`.
        clues (List[ClueType]): List of clues to explain `value`.
        children: (List[ChildConnection] or None):
    """

    lid: str = Field(default_factory=lambda: str(uuid.uuid4()))
    value: Optional[ValueType]
    clues: List[ClueType] = []
    children: Optional[List[ChildConnection]] = None

    class Config:
        smart_union = True


class LabelFeedback(Label):
    """
    Feedback on a label value. See ``Feedback`` for more information.

    Attributes:
        source: Identifies the source of a ``Feedback``.
        vote: Defines if `Label.value` should be considered True or False.

    Remarks:
        - When field holds multiple values (see ``Automatisme.prediction_schema``),
          a value 'Z' can be invalidated by sharing a ``LabelFeedback``
          with ``LabelFeedback.vote == FeedbackVote.VALID`` and ``LabelFeedback.value == 'Z'``.
        - When a field holds a single value, it can be invalidated by simply sharing a new
          value or by invalidating it when a value is invalidated, it does not appear
          in ``Target.current``.
    """

    source: Optional[str] = FEEDBACK_M2M_IDENTIFIER
    vote: FeedbackVote = FeedbackVote.VALID


class LabelPrediction(Label):
    """
    Minimal data structure used in ``Prediction``, containing a single prediction.
    ``Prediction.result[key]`` is either a ``LabelPrediction`` or a list of ones.

    Attributes:
        score (float, None): score of the prediction between 0 and 100
        model_version (str, None): version of the model used for the prediction
        children (Optional[str]): points to documents resulting of a split of the
            original document.
    """

    score: Optional[float] = Field(None, ge=0, le=100)
    model_version: Optional[str] = None


CurrentValueType = Union[List[Label], Label]
"""As well as ``PredictionValueType`` describes the basic types of prediction values
and ``FeedbackValueType`` describes the basic types of feedback values, CurrentValueType
describes the basic types of predicted values after feedbacks have been taken in account:
a ``Label`` or a list of ones. More complex values are reprensented as ``CurrentResultType``
objects."""


class CurrentResultType(BaseModel):
    """
    General representation or the result of a prediction when feedbacks have been taken
    into account. For this reason, its structure is a mirror of ``PredictionResultType``.
    It is defined as a nested dict-like object associating string keys to:

        - a ``CurrentValueType`` if the correct value is a single primitive object (e.g.
          a boolean, a string, or and integer or a float) or a list of ones. In such a
          case, each value is stored in a ``Label`` object.
        - A list or a list of list of ``CurrentValueType``
        - Another ``CurrentResultType`` or a list of ones if the structure of the
          correction value is more complex.

    See ``Current`` for more information.

    Attributes:
        __root__:
    """

    __root__: Dict[
        str,
        Union[
            List["CurrentResultType"],
            "CurrentResultType",
            List[List[CurrentValueType]],
            List[CurrentValueType],
            CurrentValueType,
        ],
    ] = {}


CurrentResultType.update_forward_refs()


class Current(BaseModel):
    """
    Define the current value of a target list of labels based on ``Prediction`` and ``Feedback``.

    Define the state of a ``Prediction`` after ``Feedback`` has been taken into account.
    For this reason, its structure is a mirror or ``Prediction`` and is basically a
    collection of ``Label`` objects. See ``CurrentResultType`` for more information.

    Attributes:
        result (CurrentResultType):
    """

    result: CurrentResultType = CurrentResultType()


PredictionValueType = Union[List[LabelPrediction], LabelPrediction]
"""Define basic types for prediction values as ``LabelPrediction`` or list of ones.
More complex values reprsented as ``PredictionResultType`` objects."""


class PredictionResultType(BaseModel):
    """
    General representation of the result of a prediction. To ensure that as many prediction
    structure can  be handled, a ``Prediction`` result is defined as a nested dict-like object
    associating string keys to:

        - A ``PredictionValueType`` if the predicted value is a single primitive object (e.g.
          a boolean, a string, or and integer or a float) or a list of ones. In such a
          case, each value is stored in a ``LabelPrediction`` object.
        - A list or a list of list of ``PredictionValueType``.
        - Another ``PredictionResultType`` or a list of ones if the structure of the
          prediction value is more complex.

    See ``Prediction`` for more information.

    Attributes:
        __root__:
    """

    __root__: Dict[
        str,
        Union[
            List["PredictionResultType"],
            "PredictionResultType",
            List[List[PredictionValueType]],
            List[PredictionValueType],
            PredictionValueType,
        ],
    ] = {}


PredictionResultType.update_forward_refs()


class Prediction(BaseModel):
    """
    AI-models prediction attached to a ``Target`` document.

    Generally speaking, a prediction is a nested collection of ``LabelPrediction``
    objects. See ``PredictionResultType`` for more information.

    Example:

        ::

            {                                                                   # Prediction
                "model_version": "v0.0",
                "score": None,
                "comment": "",
                "result": {                                                     # PredictionResultType
                    "date": {                                                   # LabelPrediction
                        "lid": "3aeb2502-8bc4-473d-a143-4874f9919c4c",
                        "value": 1579474800,
                        "clues": [],
                        "score": None,
                        "model_version": None,
                        "children": None,
                    },
                    "first names": [                                            # List[LabelPrediction]
                        {                                                       # LabelPrediction
                            "lid": "09aa9edc-373e-4896-804c-74241813db06",
                            "value": "Bohrn",
                            "clues": [],
                            "score": 0.0,
                            "model_version": None,
                            "children": None,
                        },
                        {                                                       # LabelPrediction
                            "lid": "d66f48a0-980c-43ae-a60d-686a48628191",
                            "value": "Einstein",
                            "clues": [],
                            "score": 100.0,
                            "model_version": None,
                            "children": None,
                        },
                    ]
                }
            }

    Attributes:
        model_version (str, None): Version of the model.
        score (float, None): Overall prediction score (from 0 to 100).
        comment (str): Comment related to prediction.
        result (PredictionResultType): Content of the prediction.

    Remarks:
      - The keys in result should match the ``PredictionSchema`` in the Automatisme
        config, see ``request.document.prediction_post_prediction``.
      - If the key in result does not match the keys in `PredictionSchema` no
        error is raised.

    Todo:
        unit tests
    """

    model_version: Optional[str] = None
    score: Optional[float] = Field(None, ge=0, le=100)
    comment: str = ""
    result: PredictionResultType = PredictionResultType()


FeedbackValueType = Union[List[LabelFeedback], LabelFeedback]
"""As well as ``PredictionValueType`` describes the basic types a prediction values,
FeedbackValueType describes the basic types of feedback values: ``LabelFeedback` or
a list of ones. More complex values are reprensented as ``FeedbackResultType``
objects."""


class FeedbackResultType(BaseModel):
    """
    General representation for the result of a label feedback. To ensure that feedbacks
    can relate to any section or subsection of the prediction it is attached to, its
    structure is a mirror of ``PredictionResultType``. It is defined as a nested dict-like
    object associating string keys to:

        - a ``FeedbackValueType`` if the correct value is a single primitive object (e.g.
          a boolean, a string, or and integer or a float) or a list of ones. In such a
          case, each new value is stored in a ``LabelFeedback`` object.
        - A list or a list of list of ``FeedbackValueType``.
        - Another ``FeedbackResultType`` or a list of ones if the structure of the
          correction value is more complex.

    See ``Feedback`` for more information.

    Attributes:
        __root__:
    """

    __root__: Dict[
        str,
        Union[
            List["FeedbackResultType"],
            "FeedbackResultType",
            List[List[FeedbackValueType]],
            List[FeedbackValueType],
            FeedbackValueType,
        ],
    ] = {}


FeedbackResultType.update_forward_refs()


class Feedback(BaseModel):
    """
    Contain aggregated confirmations, deletions or modifications for a ``Prediction`` values.

    Generally speaking, a Feedback is a nested collection of ``LabelFeedback``. See
    ``FeedbackResultType`` for more information.

    Example:

        Correction of the example given in ``Prediction``:

        ::

            {
                "comment": "no comment"
                "result": {
                    "date": {                                                   # LabelFeedback: confirmation
                        "lid": "3aeb2502-8bc4-473d-a143-35594753u299",
                        "value": "1579474800"
                        "clue": []
                        "children": None,
                        "source": "M2M"
                        "vote": "Valid",
                    },
                    "first names": [
                        {                                                       # LabelFeedback: modification
                            "lid": "3aeb2502-8bc4-473d-a143-35594753u299",
                            "value": "Bohr"
                            "clue": []
                            "children": None,
                            "source": "M2M"
                            "vote": "Invalid",
                        },
                    ]
                }
            }

    Attributes:
        comment (str): Comment related to the feedback.
        result (FeedbackResultType): Content of the feedback.
    """

    comment: str = ""
    result: FeedbackResultType = (
        FeedbackResultType()
    )  # may be a list for type multi-class
