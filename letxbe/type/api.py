from typing import List

from pydantic import BaseModel


class FeedbackResponse(BaseModel):
    """Response returned when posting a `Feedback` on a document.

    See :obj:`letxbe.type.labels.FeedBack` for more information.

        Attributes:
            updated_labels (List[str]): List of labels whose value have been updated.
    """

    updated_labels: List[str]
