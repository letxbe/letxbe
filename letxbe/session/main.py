from typing import Dict, Optional, cast

import requests

from letxbe.exception import AuthorizationError, AutomationError, UnkownRessourceError
from letxbe.type.enum import Url

BASE_URL = "https://prod-unfold.onogone.com"


class LXBSession:
    """
    Connect to LetXbe and share requests.
    """

    def __init__(
        self, client_id: str, client_secret: str, server_address: Optional[str] = None
    ):
        self.__server_address = BASE_URL if server_address is None else server_address
        self.__token = self._connect(client_id, client_secret)

    @property
    def server(self) -> str:
        return self.__server_address

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

    @staticmethod
    def _verify_status_code(res: requests.Response) -> None:
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
    def authorization_header(self) -> Dict:
        return {"Authorization": "Bearer " + self.__token}
