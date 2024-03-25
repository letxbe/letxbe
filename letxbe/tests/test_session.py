from unittest.mock import Mock, patch

from letxbe.session import BASE_URL, create_letxbe_session
from letxbe.type.enum import Url


@patch("letxbe.main.requests.post")
def test_create_letxbe_session__authorization_header(mocked_post, mock_access_token):
    # Given
    mocked_post.return_value = Mock(
        status_code=201, json=lambda: {"access_token": "some_access_token"}
    )
    client_id = Mock()
    client_secret = Mock()

    # When
    lxb = create_letxbe_session(client_id, client_secret, BASE_URL)

    # Then
    mocked_post.assert_called_with(
        BASE_URL + Url.LOGIN,
        json={
            "client_id": client_id,
            "client_secret": client_secret,
        },
    )
    print(lxb.headers)
    assert lxb.headers["Authorization"] == f"Bearer {mock_access_token}"
