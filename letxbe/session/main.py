from typing import Dict, Optional, cast

import requests

from letxbe.exception import AuthorizationError, AutomationError, UnkownRessourceError
from letxbe.type.enum import Url

BASE_URL = "https://prod-unfold.onogone.com"


class LXBSession:
    """Base class for connection with the server.

    Alongside the server address, two informations provided by Auth0 are required to establish
    a successful connection:

        - the client identifier, referred to as ``client_id``;
        - the client password, referred to as ``client_secret``.

    When instanciated, an access token is requested to the server. If the request is accepted,
    the token (also called ``BEARER_CODE``) is returned and stored. This token will populate
    the authentication header that will allow authentication while posting or getting data
    to/from the server.

    Please note that this token is temporary: it will expire after a while.
    """

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
        self.__token = self._connect(client_id, client_secret)

    @property
    def server(self) -> str:
        """Address of the server."""
        return self.__server_address

    def _connect(self, client_id: str, client_secret: str) -> str:
        """Connect with LetXbe.

        Args:
            client_id (str): Auth0 client ID.
            client_secret (str): Auth0 client secret.

        Returns:
            str: The `BEARER_CODE` associated to the authentication.

        Raises:
            AuthorizationError: If the connection to the server is forbidden (403 Forbidden).
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

    @staticmethod
    def _verify_status_code(res: requests.Response) -> None:
        """Map the status code of the response of the request to a Python
        exception and raise it (if any).

        Args:
            res (requests.Reponse): Response of a request.

        Raises:
            AuthorizationError: If the connection to the server is forbidden (403 Forbidden).
            UnkownRessourceError: If the requested ressource is not found (404 Not Found).
            AutomationError: If the server is facing a internal error (500 Internal Server Error).
            ValueError: If the server returns any other error code.
        """

        if res.status_code == 403:
            raise AuthorizationError(res.reason)

        if res.status_code == 404:
            raise UnkownRessourceError(res.reason)

        if res.status_code == 500:
            raise AutomationError(res.reason)

        if res.status_code == 200:
            return

        raise ValueError(f"Request failed with code {res.status_code}: {res.reason}")

    @property
    def authorization_header(self) -> Dict[str, str]:
        """Header for authenticating API calls. Authentication is done via a Bearer code."""
        return {"Authorization": "Bearer " + self.__token}
