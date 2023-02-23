import uuid
from typing import Dict, List, Optional, Union

from pydantic import BaseModel, Field

from .base import ValueType
from .enum import FeedbackVote

FEEDBACK_M2M_IDENTIFIER = "M2M"


class ClueMixin(BaseModel):
    """
    Define shared information between all clue formats.

    Args:
        role (str, None): Role of the Artefact that contains the source.
            If 'None', the document is the `Target` that contains
            the prediction or feedback where the Clue is saved.
    """

    role: Optional[str]


class PageClue(ClueMixin):
    """
    Point to a page in a document.

    Args:
        page_idx: Page index of a page in an original document.

    Remarks:
        if a document is a split version of an original one, page_idx is the page index
            of the page in the original document.
    """

    page_idx: int


class ProjectionClue(ClueMixin):
    """
    Contains information to extract a `ProjectionField` from a Document.

    Args:
        pkey (str): key pointing to a list of `ProjectionRoot`
        xid (str): xid of the ProjectionRoot
        projection_entry (str): see `__ProjectionBase.projection_entry`
        # TODO rename this to `projection_path`

    Examples:
        (without recursive structure) document.projection[pkey]
            -> filter projection_root_list by `xid`
            -> output projection_root.result[projection_entry]
        (with recursive structure) # TODO add example
    """

    pkey: str
    xid: str
    projection_entry: str


ClueType = Union[PageClue, ProjectionClue]


class Label(BaseModel):
    """
    Information produced about a `Target` and its connected `Artefact` documents,

    Args:
        lid: a unique identifier for the Label
        value: Information on the label.
          There can be only one Label with the same `value` in a `multiple prediction field`
        clues: List of ClueType objects to explain `value`
    """

    lid: str = Field(default_factory=lambda: str(uuid.uuid4()))
    value: Optional[ValueType]
    clues: List[ClueType] = []

    class Config:
        smart_union = True


class LabelFeedback(Label):
    """
    Args:
        source: identifies the source of a `Feedback`.
        vote: defines if `Label.value` should be considered True or False

    Remarks:
        when field holds multiple values (see `Automatisme.prediction_schema`),
            a value 'Z' can be invalidated by sharing a `LabelFeedback`
            with `LabelFeedback.vote` == FeedbackVote.VALID and `LabelFeedback.value`
            is 'Z'
        when a field holds a single value, it can be invalidated by simply sharing a new
            value or by invalidating it
        when a value is invalidated, it does not appear in `Target.current`
    """

    source: Optional[str] = FEEDBACK_M2M_IDENTIFIER
    vote: FeedbackVote = FeedbackVote.VALID


class ChildConnection(BaseModel):
    atms_slug: str
    doc_slug: str


class LabelPrediction(Label):
    """
    Minimal data structure used in `Prediction`, containing a single prediction.

    `Prediction.result[key]` is either a `LabelPrediction` or a list of `LabelPrediction`.

    Args:
        score (float, None): score of the prediction between 0 and 100
        model_version (str, None): version of the model used for the prediction
        children (Optional[str]): points to documents resulting of a split of the
            original document.
    """

    score: Optional[float] = Field(None, ge=0, le=100)
    model_version: Optional[str] = None
    children: Optional[List[ChildConnection]] = None


CurrentValueType = Union[List[Label], Label]


class CurrentResultType(BaseModel):
    __root__: Dict[
        str, Union[CurrentValueType, List["CurrentResultType"], "CurrentResultType"]
    ] = {}


CurrentResultType.update_forward_refs()


class Current(BaseModel):
    """
    Define the current value of a target list of labels based on Prediction and Feedback
    """

    result: CurrentResultType = CurrentResultType()


PredictionValueType = Union[List[LabelPrediction], LabelPrediction]


class PredictionResultType(BaseModel):
    __root__: Dict[
        str,
        Union[
            List["PredictionResultType"], "PredictionResultType", PredictionValueType
        ],
    ] = {}


PredictionResultType.update_forward_refs()


class Prediction(BaseModel):
    """
    Output typing related to AI-models predictions.

    Args:
        model_version (str, None): version of the model
        score (float, None): overall prediction score (from 0 to 100)
        comment (str): comment related to prediction
        result (Dict[str, Union[List[LabelPrediction], LabelPrediction]]): see
            `LabelPrediction`.

    Remarks:
        the keys in result must match the `PredictionSchema` in the Automatisme
            config, see `request.document.prediction_post_prediction`
        if the key in result does not match the keys in `PredictionSchema` no
            error is raised
    """

    model_version: Optional[str] = None
    score: Optional[float] = Field(None, ge=0, le=100)
    comment: str = ""
    result: PredictionResultType = PredictionResultType()


FeedbackValueType = Union[List[LabelFeedback], LabelFeedback]


class FeedbackResultType(BaseModel):
    __root__: Dict[
        str, Union[FeedbackValueType, List["FeedbackResultType"], "FeedbackResultType"]
    ] = {}


FeedbackResultType.update_forward_refs()


class Feedback(BaseModel):
    """
    Contain aggregated confirmations, deletions or modifications for a `Prediction` values.
    """

    comment: str = ""
    result: FeedbackResultType = (
        FeedbackResultType()
    )  # may be a list for type multi-class
