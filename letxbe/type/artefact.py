"""

An `Artefact` is a `Document` that provides additional information when handling `Target` documents.

"""
from typing import Dict

from pydantic import BaseModel, Field

from .base import SlugMixin
from .document import DocumentMixin, StatusMixin, WithParentMixin


class ArtefactMixin(BaseModel):
    """Information specific to an `Artefact`_.

    Attributes:
        role (str): Uniquely identify the artefact as document connected to another
        document. It is chosen during set-up.
    """

    role: str = Field(..., min_length=1)


class ArtefactToConnect(SlugMixin):
    """Information that is enough to connect an artefact to other documents when uploading them.
    Essentially a `SlugMixin`_ referencing an `Document`_ of specific type `Artefact`_."""


class WithArtefactsMixin(BaseModel):
    """Capacity to connect a document to a series of artefacts when uploading it.

    Keys in ``WithArtefactsMixin.artefact`` are defined in the `Automatisme` configuration.

    Attributes:
        artefact (Dict[str, ArtefactToConnect]):
    """

    artefact: Dict[str, ArtefactToConnect] = {}


class ConnectedArtefact(DocumentMixin, ArtefactMixin, WithParentMixin, StatusMixin):
    """Information about an `Artefact`_ that is available when accessing another `Document`_
    the artefact is connected to."""


class ArtefactConnectionMixin(BaseModel):
    """Capacity for a document to provide information about connected `Artefact`_ documents.

    Keys in ``ArtefactConnectionMixin.artefact`` are defined in the `Automatisme` configuration.

    Attributes:
        artefact (Dict[str, ConnectedArtefact]):

    Todo:
        Add a validator to ensure role in Dict is equal to ConnectedArtefact.role
    """

    artefact: Dict[str, ConnectedArtefact] = {}


class Artefact(
    DocumentMixin, ArtefactMixin, WithParentMixin, StatusMixin, ArtefactConnectionMixin
):
    """Document sent to letxbe to be connected to one or multiple `Target`_."""
