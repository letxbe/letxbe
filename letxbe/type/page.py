"""
Core typing classes describing text spatially structured.

Examples:
     a pdf parsed into a list of `Page`
     the screenshot of web-page parsed into a list of `Lines`
"""

from enum import Enum
from typing import List, Optional, Tuple

from pydantic import BaseModel, Field

BBOX_SCALE = 1
MIN_BBOX_OVERLAP_PROPORTION = 0.7


class ImageFormat(str, Enum):
    PNG = "png"
    JPEG = "jpeg"
    JPG = "jpg"
    TIFF = "tiff"


class ImageProperties(BaseModel):
    size: List[int] = Field(..., min_items=2, max_items=2)
    format: ImageFormat = ImageFormat.PNG
    rotation: float = 0.0

    class Config:
        use_enum_values = True


class BBox(BaseModel):
    x0: float = Field(..., ge=0, le=BBOX_SCALE)
    x1: float = Field(..., ge=0, le=BBOX_SCALE)
    y0: float = Field(..., ge=0, le=BBOX_SCALE)
    y1: float = Field(..., ge=0, le=BBOX_SCALE)

    @property
    def width(self) -> float:
        return self.x1 - self.x0

    @property
    def height(self) -> float:
        return self.y1 - self.y0

    @property
    def center(self) -> Tuple[float, float]:
        return (self.x0 + self.x1) / 2, (self.y0 + self.y1) / 2

    @property
    def area(self) -> float:
        return self.width * self.height

    @classmethod
    def from_tuple(cls, values: Tuple[float, float, float, float]) -> "BBox":
        x0, y0, x1, y1 = values
        return cls.parse_obj({"x0": x0, "x1": x1, "y0": y0, "y1": y1})

    def to_tuple(self) -> Tuple[float, float, float, float]:
        return self.x0, self.y0, self.x1, self.y1

    def x_overlap_with(
        self, bbox: "BBox", threshold: float = MIN_BBOX_OVERLAP_PROPORTION
    ) -> bool:
        overlap = min(self.x1, bbox.x1) - max(self.x0, bbox.x0)
        min_width = min(self.width, bbox.width)

        return overlap > threshold * min_width

    def y_overlap_with(
        self, bbox: "BBox", threshold: float = MIN_BBOX_OVERLAP_PROPORTION
    ) -> bool:
        overlap = min(self.y1, bbox.y1) - max(self.y0, bbox.y0)
        min_height = min(self.height, bbox.height)

        return overlap > threshold * min_height

    def contain(self, bbox: "BBox") -> bool:
        if self.x0 > bbox.x0 or self.x1 < bbox.x1:
            return False
        if self.y0 > bbox.y0 or self.y1 < bbox.y1:
            return False
        return True


class Word(BaseModel):
    word_caption: str = Field(..., alias="word-caption")
    bbox: BBox
    confidence: float = Field(..., ge=0, le=100)

    # ref to deal with aliases https://pydantic-docs.helpmanual.io/usage/model_config/
    class Config:
        allow_population_by_field_name = True


class Line(BaseModel):
    bbox: BBox
    words: List[Word]
    line_caption: str = Field(..., alias="line-caption")
    rotation: Optional[float] = Field(None, ge=-180, le=180)
    confidence: float = Field(..., ge=0, le=100)

    class Config:
        allow_population_by_field_name = True


class Page(BaseModel):
    file_uri: str
    page_idx: int
    line_list: List[Line]
    image_properties: Optional[ImageProperties] = None

    class Config:
        arbitrary_types_allowed = True
