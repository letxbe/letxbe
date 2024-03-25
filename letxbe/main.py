import json
from typing import Dict, Optional, Tuple, Union

import requests

from letxbe.exception import (
    AutomationError,
    ForbiddenError,
    UnauthorizedError,
    UnknownResourceError,
)
from letxbe.session import BASE_URL, create_letxbe_session
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


class LXB:
    """Connection session to LetXbe. Provides methods for posting or
    requesting documents, artefacts, predictions and feedbacks."""

    def __init__(
        self, client_id: str, client_secret: str, server_address: Optional[str] = None
    ):
        """
        Args:
            client_id (str): Auth0 client ID.
            client_secret (str): Auth0 client secret.
            server_address (str, optional): Address of the server.
                If None or not specified, `BASE_URL` will be used by default.
        """
        self.__server_address = BASE_URL if server_address is None else server_address
        self.__session = create_letxbe_session(
            client_id, client_secret, self.__server_address
        )

    @property
    def server(self) -> str:
        """Address of the server."""
        return self.__server_address

    @staticmethod
    def _verify_status_code(res: requests.Response) -> None:
        """Map the response status code to a Python exception and raise it (if any).

        Args:
            res (requests.Response): Response of a request.

        Raises:
            ForbiddenError: connection to the server is forbidden (403 Forbidden).
            UnknownResourceError: the requested resource is not found (404 Not Found).
            AutomationError: the server is facing an internal error (500 Internal Server Error).
            ValueError: if the server returns any other error code.
        """
        if res.status_code == 401:
            raise UnauthorizedError(f"401 in response: {res}")

        if res.status_code == 403:
            raise ForbiddenError(f"403 in response: {res}")

        if res.status_code == 404:
            raise UnknownResourceError(f"404 in response: {res}")

        if res.status_code == 500:
            raise AutomationError(f"500 in response: {res}")

        if res.status_code == 200:
            return

        raise ValueError(f"Request failed with code {res.status_code}: {res}")

    def _post_document(
        self,
        route: str,
        metadata: Metadata,
        file: Optional[Tuple[str, bytes]],
        slug: Optional[str] = None,
    ) -> str:
        """Post a document.

        Should only be used directly if you know what you're doing concerning the route.

        Args:
            route (str): URL to post the document to.
            metadata (Metadata): Document metadata.
            file (Tuple[str, bytes], optional): Filename and bytes to post for a File.

        Returns:
            str: Text of the HTTP response.
        """
        files: Dict[str, Tuple[str, Union[str, bytes]]] = {}
        if file is not None:
            files["file"] = file

        metadata_dict = pydantic_model_to_json(metadata)
        if slug is not None:
            metadata_dict["slug"] = slug

        response = self.__session.post(
            url=route,
            files=files,
            data={
                "metadata": json.dumps(metadata_dict),
            },
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
        """Post a target.

        Args:
            automatisme_slug (str): Slug of the automatisme.
            metadata (Metadata): Metadata of the target.
            file (Tuple[str, bytes], optional): Filename and bytes to post as a Target.

        Returns:
            str: Slug of the new document.
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
        """Post an artefact.

        Args:
            automatisme_slug (str): Slug of the automatisme.
            role (str): Role of the artefact.
            metadata (Metadata): Metadata of the artefact.
            file (Tuple[str, bytes], optional): Filename and bytes to post as an Artefact.

        Returns:
            str: Slug of the new document.
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
        """Post a prediction to a given document.

        Args:
            automatisme_slug (str): Slug of the automatisme.
            document_slug (str): Slug of the document.
            prediction (Prediction): Contents of the prediction.
        """
        response = self.__session.post(
            url=self.server
            + Url.POST_PREDICTION.format(
                automatisme_slug=automatisme_slug, document_slug=document_slug
            ),
            data=json.dumps(prediction.dict()),
        )

        self._verify_status_code(response)

        return None

    def post_feedback(
        self,
        automatisme_slug: str,
        document_slug: str,
        feedback: Feedback,
    ) -> FeedbackResponse:
        """Post a feedback to a given document.

        Args:
            automatisme_slug (str): Slug of the automatisme.
            document_slug (str): Slug of the document.
            feedback (Feedback): Contents of the feedback.

        Returns:
            FeedbackResponse: The response containing the updated labels.
        """
        response = self.__session.post(
            url=self.server
            + Url.POST_FEEDBACK.format(
                automatisme_slug=automatisme_slug, document_slug=document_slug
            ),
            data=json.dumps(feedback.dict()),
        )

        self._verify_status_code(response)

        return FeedbackResponse.parse_obj(response.json())

    def get_document(
        self,
        automatisme_slug: str,
        document_slug: str,
    ) -> Union[Artefact, Target]:
        """Get a document or artefact corresponding to a document slug.

        Args:
            automatisme_slug (str): Slug of the automatisme.
            document_slug (str): Slug of the document.

        Returns:
            Union[Artefact, Target]: The document or artefact corresponding to
            the document slug.
        """

        response = self.__session.get(
            url=self.server
            + Url.GET_DOCUMENT.format(
                automatisme_slug=automatisme_slug, document_slug=document_slug
            ),
        )

        self._verify_status_code(response)

        document_metadata = response.json()
        if "role" in document_metadata and document_metadata["role"] is not None:
            return Artefact.parse_obj(document_metadata)
        return Target.parse_obj(document_metadata)
