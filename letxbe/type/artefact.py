"""

An `Artefact` is a `Document` that provides additional information when handling `Target` documents.

"""
from typing import Dict

from pydantic import BaseModel, Field

from .base import SlugMixin
from .document import DocumentMixin, StatusMixin, WithParentMixin


class ArtefactMixin(BaseModel):
    """
    Information specific to an `Artefact`.
    """

    role: str = Field(..., min_length=1)


class ArtefactToConnect(SlugMixin):
    """
    Information that is enough to connect an `Artefact` to other documents when uploading them.
    """


class WithArtefactsMixin(BaseModel):
    """
    Capacity to connect a document to a series of artefacts when uploading it.

    Keys in `WithArtefactsMixin.artefact` are defined in the `Automatisme` configuration.
    """

    artefact: Dict[str, ArtefactToConnect] = {}


class ConnectedArtefact(DocumentMixin, ArtefactMixin, WithParentMixin, StatusMixin):
    """
    Information about an `Artefact` that is available when accessing another `Document`
    the `Artefact` is connected to.
    """


class ArtefactConnectionMixin(BaseModel):
    """
    Capacity for a document to provide information about connected `Artefact` documents.

    Keys in `ArtefactConnectionMixin.artefact` are defined in the `Automatisme` configuration.

    # TODO : add a validator to ensure role in Dict is equal to ConnectedArtefact.role
    """

    artefact: Dict[str, ConnectedArtefact] = {}


class Artefact(
    DocumentMixin, ArtefactMixin, WithParentMixin, StatusMixin, ArtefactConnectionMixin
):
    """
    Information about an `Artefact` that is available when accessing it directly.
    """
