from typing import List

from pydantic import BaseModel


class FeedbackResponse(BaseModel):
    """Response returned when posting a `Feedback`_ on a document.

    Attributes:
        updated_labels (List[str]): Labels whose values have received a feedback.
    """

    updated_labels: List[str]
