from typing import List

from pydantic import BaseModel


class FeedbackResponse(BaseModel):
    updated_labels: List[str]
