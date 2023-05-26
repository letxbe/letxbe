import uuid
from typing import Dict, List, Optional, Union

from pydantic import BaseModel, Field

from .base import ValueType
from .enum import FeedbackVote
from .image import BBox

FEEDBACK_M2M_IDENTIFIER = "M2M"


class ClueMixin(BaseModel):
    """Define shared information between all clue formats.

    Attributes:
        role (str, None): Role of the Artefact that contains the source.
            If 'None', the document is the `Target` that contains
            the prediction or feedback where the Clue is saved.
    """

    value: str = ""
    role: Optional[str]


class BBoxMixin(BaseModel):
    """Normalized coordinates of a bounding box in an image.

    Attributes:
        bbox: see type.image.BBox
    """

    bbox: BBox


class PageClue(ClueMixin):
    """Point to a page in a document.

    Attributes:
        page_idx (int): Page index of a page in an original document.

    Remarks:
        If a document is a split version of an original one, page_idx is the page index
        of the page in the original document.
    """

    page_idx: int


class WordClue(PageClue):
    """Coordinates of a word in a `Page` object.

    Args:
        line_idx (int): line index
        word_idx (int): word index
    """

    line_idx: int
    word_idx: int
    bbox: Optional[BBox] = None


class BBoxInPageClue(PageClue, BBoxMixin):
    """Point to a bounding box in a page of a document.

    Args:
        page_idx: Page index of a page in an original document.
        bbox: bounding box in the corresponding image, see type.image.BBox

    Remarks:
        if a document is a split version of an original one, page_idx is the page index
            of the page in the original document.
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


ClueType = Union[ProjectionClue, BBoxInPageClue, WordClue, PageClue]


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
    Information produced about a `Target` and its connected `Artefact` documents,

    Attributes:
        lid: a unique identifier for the Label
        value: Information on the label.
            There can be only one Label with the same `value` in a `multiple prediction field`
        clues: List of ClueType objects to explain `value`
    """

    lid: str = Field(default_factory=lambda: str(uuid.uuid4()))
    value: Optional[ValueType]
    clues: List[ClueType] = []
    children: Optional[List[ChildConnection]] = None

    class Config:
        smart_union = True


class LabelFeedback(Label):
    """
    Attributes:
        source: identifies the source of a `Feedback`.
        vote: defines if `Label.value` should be considered True or False

    Remarks:
        - When field holds multiple values (see `Automatisme.prediction_schema`),
          a value 'Z' can be invalidated by sharing a `LabelFeedback`
          with `LabelFeedback.vote` == FeedbackVote.VALID and `LabelFeedback.value`
          is 'Z'.
        - When a field holds a single value, it can be invalidated by simply sharing a new
          value or by invalidating it when a value is invalidated, it does not appear
          in `Target.current`.
    """

    source: Optional[str] = FEEDBACK_M2M_IDENTIFIER
    vote: FeedbackVote = FeedbackVote.VALID


class LabelPrediction(Label):
    """
    Minimal data structure used in `Prediction`, containing a single prediction.

    `Prediction.result[key]` is either a `LabelPrediction` or a list of `LabelPrediction`.

    Attributes:
        score (float, None): score of the prediction between 0 and 100
        model_version (str, None): version of the model used for the prediction
        children (Optional[str]): points to documents resulting of a split of the
            original document.
    """

    score: Optional[float] = Field(None, ge=0, le=100)
    model_version: Optional[str] = None


CurrentValueType = Union[List[Label], Label]


class CurrentResultType(BaseModel):
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
    Define the current value of a target list of labels based on Prediction and Feedback.

    Attributes:
        result (CurrentResultType):
    """

    result: CurrentResultType = CurrentResultType()


PredictionValueType = Union[List[LabelPrediction], LabelPrediction]


class PredictionResultType(BaseModel):
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
    Output typing related to AI-models predictions.

    Attributes:
        model_version (str, None): version of the model
        score (float, None): overall prediction score (from 0 to 100)
        comment (str): comment related to prediction
        result (Dict[str, Union[List[LabelPrediction], LabelPrediction]]): see
            `LabelPrediction`.

    Remarks:
      - The keys in result must match the `PredictionSchema` in the Automatisme
        config, see `request.document.prediction_post_prediction`.
      - If the key in result does not match the keys in `PredictionSchema` no
        error is raised.
    """

    model_version: Optional[str] = None
    score: Optional[float] = Field(None, ge=0, le=100)
    comment: str = ""
    result: PredictionResultType = PredictionResultType()


FeedbackValueType = Union[List[LabelFeedback], LabelFeedback]


class FeedbackResultType(BaseModel):
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
    Contain aggregated confirmations, deletions or modifications for a `Prediction` values.

    Attributes:
        comment (str):
        result (FeedbackResultType):
    """

    comment: str = ""
    result: FeedbackResultType = (
        FeedbackResultType()
    )  # may be a list for type multi-class
