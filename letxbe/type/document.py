from typing import Dict, List, Optional, Union

from pydantic import BaseModel

from .base import ValueType, Vertex
from .enum import ActionCode, DocumentStatus

FormValueType = Union[List[ValueType], ValueType]

FormResultType = Dict[str, Optional[FormValueType]]


class Form(BaseModel):
    """
    Contains information available about a `Document` when uploading it.

    Remarks:
        can be used in multiple scenarii:
          - specifying options for an AI Model
          - attaching an `Artefact` after uploading a `Target`,
            in that case, `Target` is not processed until a matching artefact is found.
        in some cases, a file may not be attached to a `Document` as the `Form`
          holds complete information about it.
    """

    result: FormResultType = {}


class __MetadataBase(Vertex):
    """
    Information shared about a document when uploading it.

    extension: the extension of the file, eg "xlsx", "pdf",...
      should be "" when no file is shared with the document.
    name: the name to give the document.
      this property can be edited after a `Prediction` or `Feedback` is made.
      when a file is attached to a document,
        letxbe recommends to use the name of the file without the extension.
    form:

    # TODO : add edited name when exporting Target.
    """

    extension: str = ""
    name: str
    form: Form = Form()


class ParentDocument(BaseModel):
    """
    Define a relationship with a parent `Document` (`Parent`).

    Used when a `Child` document is an extract of a `Parent`.

    atms_slug: the slug of the Automatisme of the `Parent`.
    tgt_slug: the slug of the `Parent`.
    """

    atms_slug: str
    tgt_slug: str


class __WithParent(BaseModel):
    """
    Ability to be connected to a `ParentDocument`
    """

    parent: Optional[ParentDocument] = None


class __DocumentBase(__MetadataBase):
    """
    Information generated about a `Document`.

    content: a list of page indices.
      if a `Document` is a splitted version of a `Parent`,
        `Child.content` contains page indices for pages in the parent document.
        eg: content = [12, 13, 14],
          ie len(content) == 3 and content[0] == 12
    """

    content: List[int] = []
    projection: Dict[str, List[str]] = {}


class __WithStatus(BaseModel):
    """
    Define codes that indicate `Document` processing status.

    status_code: indicates pipeline processing status.
    action_code: characterizes the latest complete step.
    exception: corresponds to the latest exception met.
    """

    status_code: DocumentStatus = DocumentStatus.PROCESSING
    action_code: Optional[ActionCode] = None
    exception: Optional[str] = None
