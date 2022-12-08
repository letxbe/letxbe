import json
from typing import Dict, Optional, Tuple, Union, cast

import requests

from .exception import AuthorizationError, AutomationError, UnkownRessourceError
from .type import Artefact, Feedback, FeedbackResponse, Metadata, Target
from .type.enum import Url

BASE_URL = "https://prod-unfold.onogone.com"


class LXB:
    """
    Connect to LetXbe and share requests.
    """

    def __init__(
        self, client_id: str, client_secret: str, server_address: Optional[str] = None
    ):
        self.__server_address = BASE_URL if server_address is None else server_address
        self.__token = self._connect(client_id, client_secret)

    def _connect(self, client_id: str, client_secret: str) -> str:
        """
        Connect with LetXbe.

        Args:
            client_id (str): Auth0 client ID.
            client_secret (str): Auth0 client secret.
        Raises:
            AuthorizationError: Invalid credentials.
        """
        response = requests.post(
            self.__server_address + Url.LOGIN,
            json={
                "client_id": client_id,
                "client_secret": client_secret,
            },
        )

        if response.status_code == 403:
            raise AuthorizationError(f"Invalid credentials: {response.text}")

        return cast(str, response.json()["access_token"])

    def _verify_status_code(self, res: requests.Response) -> None:
        if res.status_code == 403:
            raise AuthorizationError(res.reason)

        if res.status_code == 404:
            raise UnkownRessourceError(res.reason)

        if res.status_code == 500:
            raise AutomationError(res.reason)

    @property
    def authorization_header(self) -> Dict:
        return {"Authorization": "Bearer " + self.__token}

    def _post_document(
        self,
        route: str,
        metadata: Metadata,
        file: Optional[Tuple[str, bytes]],
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
        files: Dict[str, Tuple[str, Union[str, bytes]]] = {
            "metadata": ("metadata.json", json.dumps(metadata.dict())),
        }
        if file is not None:
            files["file"] = file

        response = requests.post(
            url=route,
            files=files,
            headers=self.authorization_header,
        )

        self._verify_status_code(response)

        return response.json()  # type: ignore [no-any-return]

    def post_target(
        self,
        automatisme_slug: str,
        metadata: Metadata,
        file: Optional[Tuple[str, bytes]] = None,
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
            route=self.__server_address
            + Url.POST_DOCUMENT.format(automatisme_slug=automatisme_slug),
            metadata=metadata,
            file=file,
        )

    def post_artefact(
        self,
        automatisme_slug: str,
        role: str,
        metadata: Metadata,
        file: Optional[Tuple[str, bytes]] = None,
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
            route=self.__server_address
            + Url.POST_ARTEFACT.format(automatisme_slug=automatisme_slug, role=role),
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
            url=self.__server_address
            + Url.POST_FEEDBACK.format(
                automatisme_slug=automatisme_slug, document_slug=document_slug
            ),
            data=feedback.dict(),
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
            url=self.__server_address
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
