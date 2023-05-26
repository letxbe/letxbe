from .artefact import WithArtefactsMixin
from .document import MetadataMixin


class Metadata(MetadataMixin, WithArtefactsMixin):
    """
    Information about a `Document` that can be shared when uploading it.

    Attributes:
        artefact: mapper that connects roles to an `ArtefactToConnect` identifying
            an existing `Artefact`.

    Remarks:
        When uploading an `Artefact`, `role` should be specified in the endpoint.
    """
