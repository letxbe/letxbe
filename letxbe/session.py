import requests

from letxbe.exception import UnauthorizedError
from letxbe.type.enum import Url

BASE_URL = "https://prod-unfold.onogone.com"


def create_letxbe_session(
    client_id: str, client_secret: str, server_address: str
) -> requests.Session:
    """Create `requests.Session` with authorization header to connect to LetXbe.

    client_id and client_secret are used to retrieve a Bearer token. The token is used
    to instantiate the `requests.Session`. Note that the token has an expiration period.

    Args:
        client_id (str): Auth0 client ID.
        client_secret (str): Auth0 client secret.
        server_address (str): base url for the login requests

    Returns:
        requests.Session with authorization header

    Raises:
        UnauthorizedError: credentials are not valid (401 Unauthorized).
    """
    json_authorization_data = {
        "client_id": client_id,
        "client_secret": client_secret,
    }

    response = requests.post(
        server_address + Url.LOGIN,
        json=json_authorization_data,
    )

    if response.status_code == 401:
        raise UnauthorizedError(f"Invalid credentials: {response.text}")

    access_token: str = response.json()["access_token"]

    session = requests.Session()
    session.headers.update({"Authorization": f"Bearer {access_token}"})
    return session
