import json
from typing import Dict, Optional, Tuple, Union

import requests

from letxbe.session import LXBSession
from letxbe.type import (
    Artefact,
    Feedback,
    FeedbackResponse,
    Metadata,
    Prediction,
    Target,
)
from letxbe.type.enum import Url
from letxbe.utils import pydantic_model_to_json


class LXB(LXBSession):
    """
    Connect to LetXbe and share requests.
    """

    def _post_document(
        self,
        route: str,
        metadata: Metadata,
        file: Optional[Tuple[str, bytes]],
        slug: Optional[str] = None,
    ) -> str:
        """
        Post a document.

        Should only be used directly if you know what you're doing concerning the route.

        Args:
            route (str): URL to post the document to.
            metadata (Metadata): Document metadata.
            file (Tuple[str, bytes], optional): Filename and bytes to post for a File.

        Returns:
            Text of the HTTP response.
        """
        files: Dict[str, Tuple[str, Union[str, bytes]]] = {}
        if file is not None:
            files["file"] = file

        metadata_dict = pydantic_model_to_json(metadata)
        if slug is not None:
            metadata_dict["slug"] = slug

        response = requests.post(
            url=route,
            files=files,
            data={
                "metadata": json.dumps(metadata_dict),
            },
            headers=self.authorization_header,
        )

        self._verify_status_code(response)

        reponse: str = response.json()
        return reponse

    def post_target(
        self,
        automatisme_slug: str,
        metadata: Metadata,
        file: Optional[Tuple[str, bytes]] = None,
        slug: Optional[str] = None,
    ) -> str:
        """
        Post a target.

        Args:
            automatisme_slug (str): Slug of the automatisme.
            metadata (Metadata): Metadata of the target.
            file (Tuple[str, bytes], optional): Filename and bytes to post as a Target.

        Returns:
            `slug` of the new document.
        """
        return self._post_document(
            route=self.server
            + Url.POST_DOCUMENT.format(automatisme_slug=automatisme_slug),
            metadata=metadata,
            file=file,
            slug=slug,
        )

    def post_artefact(
        self,
        automatisme_slug: str,
        role: str,
        metadata: Metadata,
        file: Optional[Tuple[str, bytes]] = None,
        slug: Optional[str] = None,
    ) -> str:
        """
        Post an artefact.

        Args:
            automatisme_slug (str): Slug of the automatisme.
            role (str): Role of the artefact.
            metadata (Metadata): Metadata of the artefact.
            file (Tuple[str, bytes], optional): Filename and bytes to post as an Artefact.

        Returns:
            `slug` of the new document.
        """
        return self._post_document(
            route=self.server
            + Url.POST_ARTEFACT.format(automatisme_slug=automatisme_slug, role=role),
            metadata=metadata,
            file=file,
            slug=slug,
        )

    def post_prediction(
        self,
        automatisme_slug: str,
        document_slug: str,
        prediction: Prediction,
    ) -> None:
        """
        Post a prediction to a given document.

        Args:
            automatisme_slug (str): Slug of the automatisme.
            document_slug (str): Slug of the document.
            prediction (Prediction): Contents of the prediction.

        """
        response = requests.post(
            url=self.server
            + Url.POST_PREDICTION.format(
                automatisme_slug=automatisme_slug, document_slug=document_slug
            ),
            data=json.dumps(prediction.dict()),
            headers=self.authorization_header,
        )

        self._verify_status_code(response)

        return None

    def post_feedback(
        self,
        automatisme_slug: str,
        document_slug: str,
        feedback: Feedback,
    ) -> FeedbackResponse:
        """
        Post a feedback to a given document.

        Args:
            automatisme_slug (str): Slug of the automatisme.
            document_slug (str): Slug of the document.
            feedback (Feedback): Contents of the feedback.

        Returns:
            FeedbackResponse object containing a list of updated labels.
        """
        response = requests.post(
            url=self.server
            + Url.POST_FEEDBACK.format(
                automatisme_slug=automatisme_slug, document_slug=document_slug
            ),
            data=json.dumps(feedback.dict()),
            headers=self.authorization_header,
        )

        self._verify_status_code(response)

        return FeedbackResponse.parse_obj(response.json())

    def get_document(
        self,
        automatisme_slug: str,
        document_slug: str,
    ) -> Union[Artefact, Target]:

        response = requests.get(
            url=self.server
            + Url.GET_DOCUMENT.format(
                automatisme_slug=automatisme_slug, document_slug=document_slug
            ),
            headers=self.authorization_header,
        )

        self._verify_status_code(response)

        document_metadata = response.json()
        if "role" in document_metadata and document_metadata["role"] is not None:
            return Artefact.parse_obj(document_metadata)
        return Target.parse_obj(document_metadata)
