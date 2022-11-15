from typing import Dict, List, Optional, Union

from pydantic import BaseModel

from .base import SlugMixin, ValueType
from .enum import ActionCode, ClientEnv, DocumentStatus

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


class MetadataMixin(BaseModel):
    """
    Information shared about a document when uploading it.

    client_env: Environment the document should be sent to (test, prod)
    extension: Extension of the file, eg "xlsx", "pdf",...
      should be "" when no file is shared with the document.
    name: Name to give the document, if you want to override a file's name
      this property should not end with an extension
      this property can be edited after a `Prediction` or `Feedback` is made.
    form: a Form object

    # TODO : ensure name doesn't end with an extension when uploading a file,
        or weird behaviors will appear when trying to download it later
    """

    client_env: ClientEnv = ClientEnv.TEST
    name: Optional[str] = None
    form: Form = Form()


class ParentDocument(BaseModel):
    """
    Define a relationship with a parent `Document` (`Parent`).

    Used when a `Child` document is an extract of a `Parent`.

    atms_slug: Slug of the Automatisme of the `Parent`.
    doc_slug: Slug of the `Parent`.
    content: list `page_idx` values for `Page` objects from Parent.content,
        when they should be considered as elements of Child.content.
    projection: map lists of `xid` values for `ProjectionRoot` objects from Parent.projection,
        when they should be considered as elements of Child.projection.
    """

    atms_slug: str
    doc_slug: str
    content: List[int] = []
    projection: Dict[str, List[str]] = {}


class WithParentMixin(BaseModel):
    """
    Ability to be connected to a `ParentDocument`
    """

    parent: Optional[ParentDocument] = None


class StatusMixin(BaseModel):
    """
    Define codes that indicate `Document` processing status.

    status_code: indicates pipeline processing status.
    action_code: characterizes the latest complete step.
    exception: corresponds to the latest exception met.
    """

    status_code: DocumentStatus = DocumentStatus.PROCESSING
    action_code: Optional[ActionCode] = None
    exception: Optional[str] = None


class DocumentMixin(SlugMixin, MetadataMixin):
    """
    Information generated about a `Document`.
    """

    name: str
