from pydantic import BaseModel, Field

BBOX_SCALE = 1000


class BBox(BaseModel):
    """
    Attributes:
        x0 (float):
        x1 (float):
        y0 (float):
        y1 (float):
    """

    x0: float = Field(..., ge=0, le=BBOX_SCALE)
    x1: float = Field(..., ge=0, le=BBOX_SCALE)
    y0: float = Field(..., ge=0, le=BBOX_SCALE)
    y1: float = Field(..., ge=0, le=BBOX_SCALE)
