from typing import List

from pydantic import BaseModel


class FeedbackResponse(BaseModel):
    # TODO finish documentation
    updated_labels: List[str]
