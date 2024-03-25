from typing import Any, Dict, List, Optional, Tuple, Union

from pydantic import BaseModel, root_validator

from letxbe.type.page import BBox


class ClueMixin(BaseModel):
    """Attributes common to all clues.

    Attributes:
        value (str): Clue value (usually the one shown in Front)
        role (str or None):  Role of (or reference to) the document that contains the
            clue. If the clue comes from its attached document, then the value must be
            `None`. Else the value must be a reference to the artefact containing the
            clue (see artefacts keys in ``ArtefactConnectionMixin``).
    """

    value: str = ""
    role: Optional[str] = None


class BBoxMixin(BaseModel):
    """Normalized coordinates of a bounding box in an image.

    Attributes:
        bbox (BBox): Bounding box (see provider.type.page.BBox).
    """

    bbox: BBox


class PageClue(ClueMixin):
    """Point to a page in a document.

    Attributes:
        page_idx (int): Page index of a page in an original document.

    Remarks:
        If a document is a split version of an original one, `page_idx` is the
        page index of the page in the original document.
    """

    page_idx: int


class WordClue(PageClue):
    """Coordinates of a word in a `Page` object.

    Attributes:
        line_idx (int): Line index.
        word_idx (int): Word index.
        bbox (Optional[BBox]): Normalized coordinates of a bounding box in an image.
            See provider.type.page.BBox.
    """

    line_idx: int
    word_idx: int
    bbox: Optional[BBox] = None


class BBoxInPageClue(PageClue, BBoxMixin):
    """Point to a bounding box in a page of a document."""


class ShapeClue(BBoxInPageClue):
    """`polygon` follows COCO convention https://cocodataset.org/#format-data

    A `ShapeClue` which is a rectangle has `polygon == []`.

    Example:
        polygon = [x1, y1, x2, y2, ..., xn, yn]
    """

    polygon: List[Tuple[float, ...]] = []

    @root_validator
    def validate_polygon(cls: Any, values: Dict) -> Dict:
        polygon = values.get("polygon", [])
        if len(polygon) in {1, 2}:
            raise ValueError("A polygon must have at least three points")

        if len(polygon) % 2 == 1:
            raise ValueError("Polygon must have an even number of elements")

        return values


class ProjectionClue(ClueMixin):
    """Path to extract a `ProjectionField` from a Document.

    Attributes:
        pkey (str): Key pointing to a list of `ProjectionRoot`
        xid (str): xid of the ProjectionRoot
        projection_entry (str): See `__ProjectionBase.projection_entry`  # TODO rename this to `projection_path`
        token_idx (int): index of the first character of the token if it is a string, else 0
        length (int): length of the token if it is a string, else 0

    Examples:
      - (without recursive structure) document.projection[pkey]
          - filter projection_root_list by `xid`
          - output projection_root.result[projection_entry]
      - (with recursive structure) # TODO add example
    """

    pkey: str
    xid: str
    projection_entry: str
    token_idx: int = 0
    length: int = 0


ClueType = Union[ProjectionClue, WordClue, BBoxInPageClue, PageClue]
"""Types of clues used in labels. See ``ProjectionClue``, ``BBoxInPageClue``,
``WordClue``, ``PageClue`` and ``Label`` for mor information."""
