from typing import Dict, List, Optional, Union

from pydantic import BaseModel

from .base import CreatedMixin, SlugMixin, ValueType
from .enum import ActionCode, ClientEnv, DocumentStatus

FormValueType = Union[List[ValueType], ValueType]


class FormResultType(BaseModel):
    """Dict-like object with:

    - keys with string format
    - values with `FormValueType` format
    """

    __root__: Dict[str, Optional[Union[FormValueType, "FormResultType"]]] = {}


FormResultType.update_forward_refs()


class Form(BaseModel):
    """Contains information available about a `Document` when uploading it.

    Args:
        result (FormResultType):

    Remarks:
      - Can be used in multiple scenarii:
          - specifying options for an AI Model
          - attaching an `Artefact` after uploading a `Target`,
            in that case, `Target` is not processed until a matching artefact is found.
      - In some cases, a file may not be attached to a `Document` as the `Form`
        holds complete information about it.
    """

    result: FormResultType = FormResultType()


class MetadataMixin(BaseModel):
    """Information shared about a document when uploading it.

    Args:
        client_env (ClientEnv): Environment the document should be sent to (test, prod)

        extension (str): Extension of the file, eg "xlsx", "pdf",... Should be "" when no file
        is shared with the document.

        name (str, optional): Name to give the document, if you want to override a file's name.

              - This property should not end with an extension.
              - This property can be edited after a `Prediction` or `Feedback` is made.

        form (Form): A Form object containing information available about the document when uploading it.

    Todo:
        Ensure name doesn't end with an extension when uploading a file,
        or weird behaviors will appear when trying to download it later.
    """

    client_env: ClientEnv = ClientEnv.TEST
    name: Optional[str] = None
    form: Form = Form()
    extension: str = ""


class ParentDocument(BaseModel):
    """Define a relationship with a parent `Document` (`Parent`).
    Used when a `Child` document is an extract of a `Parent`.

    Attributes:
        atms_slug (str): Slug of the Automatisme of the `Parent`.

        doc_slug: Slug of the `Parent`.

        content: A filter that lists `page_idx` values from Parent.content `Page` objects that should be kept in Child.content.

          - If no `Page` objects should be transferred, use []
          - If all `Page` objects should be transferred, use None

        projection: a filter that lists `xid` values from Parent.projection[...] `ProjectionRoot` objects that should be kept in Child.projection

          - keys are `pkey` or `ProjectionClue`
          - If no `ProjectionRoot` objects should be transferred, use [] or do not cite `pkey` in `Parent.projection`
          - If all `ProjectionRoot` objects should be transferred, use None
    """

    atms_slug: str
    doc_slug: str
    content: Optional[List[int]] = []
    projection: Dict[str, Optional[List[str]]] = {}


class WithParentMixin(BaseModel):
    """Ability to be connected to a `ParentDocument`

    Attributes:
        parent (`ParentDocument` or None):
    """

    parent: Optional[ParentDocument] = None


class StatusMixin(BaseModel):
    """Define codes that indicate `Document` processing status.

    Attributes:
        status_code (DocumentStatus): Indicates pipeline processing status.
        action_code (ActionCode or None): Characterizes the latest complete step.
        exception (str or None): Corresponds to the latest exception met.
    """

    status_code: DocumentStatus = DocumentStatus.PROCESSING
    action_code: Optional[ActionCode] = None
    exception: Optional[str] = None


class DocumentMixin(CreatedMixin, SlugMixin, MetadataMixin):
    """Information generated about a `Document`.

    Attributes:
        name (str): `Document` name.
        urn (str): `Document` URN.
    """

    name: str
    urn: str
