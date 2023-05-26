"""
Core typing classes describing text spatially structured.

Examples:
     a pdf parsed into a list of `Page`
     the screenshot of web-page parsed into a list of `Lines`
"""
from enum import Enum
from typing import List, Optional

from pydantic import BaseModel, Field


class ImageFormat(str, Enum):
    PNG = "png"
    JPEG = "jpeg"
    JPG = "jpg"
    TIFF = "tiff"

    class Config:
        use_enum_values = True


class ImageProperties(BaseModel):
    size: List[int] = Field(..., min_items=2, max_items=2)
    format: ImageFormat = ImageFormat.PNG

    class Config:
        use_enum_values = True


class BBox(BaseModel):
    x0: float = Field(..., ge=0, le=1)
    x1: float = Field(..., ge=0, le=1)
    y0: float = Field(..., ge=0, le=1)
    y1: float = Field(..., ge=0, le=1)


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
