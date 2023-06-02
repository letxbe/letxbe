from typing import Dict, List, Optional, Union

from pydantic import BaseModel

from .base import CreatedMixin, SlugMixin, ValueType
from .enum import ActionCode, ClientEnv, DocumentStatus

FormValueType = Union[List[ValueType], ValueType]
"""Types of values used in `FormResultType`_. See also `ValueType`_ for more information."""


class FormResultType(BaseModel):
    """
    Define part of the metadata attached to a document.

    It is a nested dict containing key-value pairs, where the values can be:

        - a primitive object, see `ValueType`_
        - a list of primitive objects
        - a nested dict of the same type of `FormResultType`

    `FormResultType` is used in the `Form`_ class.

    Example:

        ::

            {
                "address": {                                # sub dict object
                    "principal": True,                      # ValueType: bool
                    "street": "41 rue Beauregard",          # ValueType: str
                    "zip code": 75002,                      # ValueType: int
                },
                "artefacts": ["customers", "orders"],       # List[ValueType]
            }

    Attributes:
        __root__:
    """

    __root__: Dict[str, Union[FormValueType, "FormResultType", None]] = {}


FormResultType.update_forward_refs()


class Form(BaseModel):
    """
    See `FormResultType`_.

    Attributes:
        result (FormResultType):
    """

    result: FormResultType = FormResultType()


class MetadataMixin(BaseModel):
    """
    Metadata attached to a document during upload.

    Attributes:
        client_env (ClientEnv): Environment the document should be sent to.
        extension (str): Extension of the file, eg "xlsx", "pdf",... Should be "" when
            no file is shared with the document.
        form (Form): See `Form`_.

    Todo:
        Ensure name doesn't end with an extension when uploading a file,
        or weird behaviors will appear when trying to download it later.

        Move extension to DocumentMixin
    """

    client_env: ClientEnv = ClientEnv.TEST
    form: Form = Form()
    extension: str = ""


class ParentDocument(BaseModel):
    """Define a relationship with a parent `Document`_ (`Parent`).
    Used when a `Child` document is an extract of a `Parent`.

    Attributes:
        atms_slug (str): Slug of the Automatisme of the `Parent`.

        doc_slug: Slug of the `Parent`.

        content: A filter that lists `page_idx` values from Parent.content `Page` objects that should be kept in Child.content.

          - If no `Page` objects should be transferred, use []
          - If all `Page` objects should be transferred, use None

        projection: a filter that lists `xid` values from Parent.projection[...] `ProjectionRoot` objects that should be kept in Child.projection

          - keys are `pkey` or `ProjectionClue`_
          - If no `ProjectionRoot` objects should be transferred, use [] or do not cite `pkey` in `Parent.projection`
          - If all `ProjectionRoot` objects should be transferred, use None
    """

    atms_slug: str
    doc_slug: str
    content: Optional[List[int]] = []
    projection: Dict[str, Optional[List[str]]] = {}


class WithParentMixin(BaseModel):
    """Ability to be connected to a `ParentDocument`_.

    Attributes:
        parent (ParentDocument or None):
    """

    parent: Optional[ParentDocument] = None


class StatusMixin(BaseModel):
    """Define codes that indicate `Document`_ processing status.

    Attributes:
        status_code (DocumentStatus): Current status in the processing pipeline.
        action_code (ActionCode or None): Latest complete step.
        exception (str or None): Latest exception met if any.
    """

    status_code: DocumentStatus = DocumentStatus.PROCESSING
    action_code: Optional[ActionCode] = None
    exception: Optional[str] = None


class DocumentMixin(CreatedMixin, SlugMixin, MetadataMixin):
    """Information generated about a `Document`_.

    Attributes:
        name (str): name given when uploading it.
        urn (str): unique file identifier used internally.
    """

    name: str
    urn: str
