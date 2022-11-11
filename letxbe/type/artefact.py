"""

An `Artefact` is a `Document` that provides additional information when handling `Target` documents.

"""
from typing import Dict

from pydantic import BaseModel, Field

from .base import Web
from .document import __DocumentBase, __MetadataBase, __WithParent, __WithStatus


class __ArtefactBase(BaseModel):
    """
    `Document` information that is specific to an `Artefact`.
    """

    role: str = Field(..., min_length=1)


class ArtefactToConnect(Web):
    """
    Information that is enough to connect an `Artefact` to other documents when uploading them.
    """


class Metadata(__MetadataBase):
    """
    Information about a `Document` that can be shared when uploading it.

    Remarks:
        When uploading an `Artefact`, `role` should be specified in the endpoint.

    artefact: a mapper that connects roles
      to an `ArtefactToConnect` identifying an existing `Artefact`.
    """

    artefact: Dict[str, ArtefactToConnect] = {}


class ConnectedArtefact(__DocumentBase, __ArtefactBase, __WithParent, __WithStatus):
    """
    Information about an `Artefact` that is available when accessing another `Document`
      the `Artefact` is connected to.
    """


class __ArtefactConnection(BaseModel):
    """
    Capacity for a document to provide information about connected `Artefact` documents.

    Keys in `__ArtefactConnection.artefact` are defined in the `Automatisme` configuration.

    # TODO : add a validator to ensure role in Dict is equal to ConnectedArtefact.role
    """

    artefact: Dict[str, ConnectedArtefact] = {}


class Artefact(
    __DocumentBase, __ArtefactBase, __WithParent, __WithStatus, __ArtefactConnection
):
    """
    Information about an `Artefact` that is available when accessing it directly.
    """
