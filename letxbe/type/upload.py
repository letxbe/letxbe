from typing import Optional

from .artefact import WithArtefactsMixin
from .document import MetadataMixin


class Metadata(MetadataMixin, WithArtefactsMixin):
    """
    Define metadata attached to a document during upload.

    Attributes:
        name (str, optional): Name to give the document, if you want to override
         a file's name. Observe that:

              - This property should not end with an extension.
              - This property can be edited after a `Prediction`_ or `Feedback`_ is made.

    Remarks:
        When uploading an `Artefact`_, `role` should be specified in the endpoint.
    """

    name: Optional[str] = None
