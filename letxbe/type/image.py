from pydantic import BaseModel, Field

BBOX_SCALE = 1000


class BBox(BaseModel):
    x0: float = Field(..., ge=0, le=BBOX_SCALE)
    x1: float = Field(..., ge=0, le=BBOX_SCALE)
    y0: float = Field(..., ge=0, le=BBOX_SCALE)
    y1: float = Field(..., ge=0, le=BBOX_SCALE)
