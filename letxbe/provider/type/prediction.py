import uuid
from enum import Enum
from typing import Any, Dict, Generator, Iterable, List, Literal, Optional, Tuple, Union

from pydantic import BaseModel, Field

from letxbe.type.base import ValueType
from letxbe.type.enum import FeedbackVote
from letxbe.type.label import PageClue as StablePageClue
from letxbe.type.label import ProjectionClue as StableProjectionClue


class LabelType(str, Enum):
    PREDICTION = "prediction"
    FEEDBACK = "feedback"

    class Config:
        use_enum_values = True


class _Clue(BaseModel):
    """
    Base class for defining clues.

    A `Clue` refers to values taken from the `Document` content or projections. Such values are
    parsed as or `ProjectionField` extracts or `Word` instances depending on the document format,
    see `type.parser`.

    Args:
        value (str): the exact value found in the document content
    """

    value: str


class PageClue(StablePageClue, _Clue):
    """
    Remarks:
        Values specified here are Optional as M2M Feedbacks do not contain this information.
    """

    line_idx: Optional[int] = None
    word_idx: Optional[int] = None


class ProjectionClue(StableProjectionClue, _Clue):
    """
    Remarks:
        Values specified here are Optional as M2M Feedbacks do not contain this information.

    Args:
        token_idx (int): index of the first character of the token in ProjectionField.value if it is a string, else 0
        length (int): length of the token in ProjectionField.value if it is a string, else 0
    """

    token_idx: Optional[int] = None
    length: int = 0


ClueType = Union[PageClue, ProjectionClue]


class Label(BaseModel):
    """
    Define an information produced about a target and its artefacts, stored in a Feedback or Prediction.

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
    label_type: Literal[LabelType.FEEDBACK] = LabelType.FEEDBACK
    source: Optional[str] = None
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
        child (Optional[str]): points to
    """

    label_type: Literal[LabelType.PREDICTION] = LabelType.PREDICTION
    score: Optional[float] = Field(None, ge=0, le=100)
    model_version: Optional[str] = None
    children: Optional[List[ChildConnection]] = None


class __Result(BaseModel):
    """
    Define properties shared by result types for `Feedback`, `Current` and `Prediction`
    """

    __root__: Dict[str, Any] = {}

    def __contains__(self, key: str) -> bool:
        return key in self.__root__

    def __iter__(self) -> Generator[Tuple[str, Any], None, None]:
        yield from self.__root__.items()

    def __len__(self) -> int:
        return len(self.__root__)

    def __delitem__(self, key: str) -> None:
        if key in self.__root__:
            del self.__root__[key]

    def keys(self) -> Iterable[str]:
        return self.__root__.keys()

    def get(self, key: str, default: Any = None) -> Optional[Any]:
        return self.__root__.get(key, default)

    def values(self) -> Iterable[Any]:
        return self.__root__.values()

    def items(self) -> Iterable[Tuple[str, Any]]:
        return self.__root__.items()


class PredictionResultType(__Result):
    __root__: Dict[str, Union[List[LabelPrediction], LabelPrediction]] = {}

    def __getitem__(self, key: str) -> Union[List[LabelPrediction], LabelPrediction]:
        return self.__root__[key]

    def __setitem__(
        self, key: str, value: Union[List[LabelPrediction], LabelPrediction]
    ) -> None:
        self.__root__[key] = value

    def get(
        self,
        key: str,
        default: Optional[Union[List[LabelPrediction], LabelPrediction]] = None,
    ) -> Optional[Union[List[LabelPrediction], LabelPrediction]]:
        return self.__root__.get(key, default)

    def values(self) -> Iterable[Union[List[LabelPrediction], LabelPrediction]]:
        return self.__root__.values()

    def items(
        self,
    ) -> Iterable[Tuple[str, Union[List[LabelPrediction], LabelPrediction]]]:
        return self.__root__.items()


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
        - the keys in result must match the `PredictionSchema` in the Automatisme
            config, see `request.document.prediction_post_prediction`
        - if the key in result does not match the keys in `PredictionSchema` no
            error is raised
    """

    model_version: Optional[str] = None
    score: Optional[float] = Field(None, ge=0, le=100)
    comment: str = ""
    result: PredictionResultType = PredictionResultType()


class FeedbackResultType(__Result):
    __root__: Dict[str, Union[List[LabelFeedback], LabelFeedback]] = {}

    def __getitem__(self, key: str) -> Union[List[LabelFeedback], LabelFeedback]:
        return self.__root__[key]

    def __setitem__(
        self, key: str, value: Union[List[LabelFeedback], LabelFeedback]
    ) -> None:
        self.__root__[key] = value

    def get(
        self,
        key: str,
        default: Optional[Union[List[LabelFeedback], LabelFeedback]] = None,
    ) -> Optional[Union[List[LabelFeedback], LabelFeedback]]:
        return self.__root__.get(key, default)

    def values(self) -> Iterable[Union[List[LabelFeedback], LabelFeedback]]:
        return self.__root__.values()

    def items(self) -> Iterable[Tuple[str, Union[List[LabelFeedback], LabelFeedback]]]:
        return self.__root__.items()


class Feedback(BaseModel):
    comment: str = ""
    result: FeedbackResultType = FeedbackResultType()
