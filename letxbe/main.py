import json
import os
from typing import Dict, Optional, Union

import requests

from letxbe.exception import AuthorizationError
from letxbe.type import (
    Artefact,
    ClientEnv,
    Feedback,
    FeedbackResponse,
    Metadata,
    Target,
    Urls,
)

BASE_URL = os.environ.get("SERVER_ADDRESS", "https://letxbe.ai")


class LXB:
    """
    Connect with LetXbe, and share requests.
    """

    def __init__(self, client_id: str, client_secret: str):
        self.__token = ""
        self._connect(client_id, client_secret)

    def _connect(self, client_id: str, client_secret: str) -> None:
        """
        Connect with LetXbe.

        Args:
            client_id (str): Auth0 client ID.
            client_secret (str): Auth0 client secret.
        Raises:
            AuthorizationError: Invalid credentials.
        """
        response = requests.post(
            BASE_URL + Urls.LOGIN,
            json={
                "client_id": client_id,
                "client_secret": client_secret,
            },
        )

        if response.status_code == 403:
            raise AuthorizationError(f"Invalid credentials: {response.text}")

        self.__token = response.json()["access_token"]

    @property
    def authorization_header(self) -> Dict:
        return {"Authorization": "Bearer " + self.__token}

    def _post_document(
        self,
        route: str,
        client_env: ClientEnv,
        metadata: Metadata,
        file: Optional[bytes],
    ) -> str:
        """
        Post a document.

        Should only be used directly if you know what you're doing concerning the route.

        Args:
            route (str): URL to post the document to.
            client_env (ClientEnv): Client environment, `test` or `prod`.
            metadata (Metadata): Document metadata.
            file (bytes, optional): File to post.

        Returns:
            Text of the HTTP response.
        """
        files: Dict[str, Union[str, bytes]] = {
            "metadata": json.dumps({**metadata.dict(), "client_env": client_env}),
        }
        if file is not None:
            files["file"] = file

        response = requests.post(
            route,
            files=files,
            headers=self.authorization_header,
        )

        return response.text  # @eligny: what is your reasoning for returning this?

    def post_target(
        self,
        automatisme_slug: str,
        client_env: ClientEnv,
        metadata: Metadata,
        file: Optional[bytes] = None,
    ) -> str:
        """
        Post a target.

        Args:
            automatisme_slug (str): Slug of the automatisme.
            client_env (ClientEnv): Client environment, `test` or `prod`.
            metadata (Metadata): Metadata of the target.  @eligny: Can you clarify the
                metadata that is expected? the Metadata class seems built for
                artefacts rather than targets
            file (bytes, optional): Binary content of the target.

        Returns:
            Text of the HTTP response.
        """
        return self._post_document(
            route=BASE_URL
            + Urls.POST_DOCUMENT.format(automatisme_slug=automatisme_slug),  # type: ignore[str-format]
            client_env=client_env,
            metadata=metadata,
            file=file,
        )

    def post_artefact(
        self,
        automatisme_slug: str,
        client_env: ClientEnv,
        role: str,
        metadata: Metadata,
        file: Optional[bytes] = None,
    ) -> str:
        """
        Post an artefact.

        Args:
            automatisme_slug (str): Slug of the automatisme.
            client_env (ClientEnv): Client environment, `test` or `prod`.
            role (str): Role of the artefact.
            metadata (Metadata): Metadata of the artefact.
            file (bytes, optional): Binary content of the artefact.

        Returns:
            Text of the HTTP response.
        """
        return self._post_document(
            route=BASE_URL
            + Urls.POST_ARTEFACT.format(automatisme_slug=automatisme_slug, role=role),  # type: ignore[str-format]
            client_env=client_env,
            metadata=metadata,
            file=file,
        )

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
            BASE_URL
            + Urls.POST_FEEDBACK.format(  # type: ignore[str-format]
                automatisme_slug=automatisme_slug, document_slug=document_slug
            ),
            data=feedback.dict(),
            headers=self.authorization_header,
        )
        return FeedbackResponse.parse_obj(response.json())

    def get_document(
        self,
        automatisme_slug: str,
        document_slug: str,
    ) -> Union[Artefact, Target]:

        response = requests.get(
            BASE_URL
            + Urls.GET_DOCUMENT.format(  # type: ignore[str-format]
                automatisme_slug=automatisme_slug, document_slug=document_slug
            ),
            headers=self.authorization_header,
        )

        document_metadata = response.json()
        if "role" in document_metadata and document_metadata["role"] is not None:
            return Artefact.parse_obj(document_metadata)
        return Target.parse_obj(document_metadata)
