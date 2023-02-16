import secrets
from unittest.mock import Mock, patch

import pytest

from letxbe.exception import AuthorizationError
from letxbe.main import LXB
from letxbe.session import BASE_URL
from letxbe.type import Metadata
from letxbe.type.enum import Url


@pytest.fixture
def mock_lxb(mock_access_token):

    with patch(
        "letxbe.main.requests.post",
        return_value=Mock(
            status_code=201, json=lambda: {"access_token": mock_access_token}
        ),
    ):
        lxb = LXB("", "")
    return lxb


@patch("letxbe.main.requests.post")
def test_lxb__auth_error(mocked_post):
    # Given
    mocked_post.return_value = Mock(status_code=403)
    client_id = "asbadf"
    client_secret = "akjhb"

    # Then
    with pytest.raises(AuthorizationError):
        LXB(client_id, client_secret)


@patch("letxbe.main.requests.post")
def test_lxb__connect_and_authorization_header(mocked_post):
    # Given
    mocked_post.return_value = Mock(
        status_code=201, json=lambda: {"access_token": "some_access_token"}
    )
    client_id = Mock()
    client_secret = Mock()

    # When
    lxb = LXB(client_id, client_secret)

    # Then
    mocked_post.assert_called_with(
        BASE_URL + Url.LOGIN,
        json={
            "client_id": client_id,
            "client_secret": client_secret,
        },
    )
    assert (
        lxb.authorization_header.get("Authorization") == "Bearer " + "some_access_token"
    )


@patch("letxbe.main.Artefact.parse_obj")
@patch("letxbe.main.Target.parse_obj")
@patch("letxbe.main.requests.get")
def test_lxb__get_document__artefact(mock_get, mock_target, mock_artefact, mock_lxb):
    # Given
    mock_get.return_value = Mock(json=lambda: {"role": "some_role"}, status_code=200)
    automatisme_slug = "atms-slug"
    document_slug = "artefact-slug"

    # When
    mock_lxb.get_document(automatisme_slug, document_slug)

    # Then
    mock_target.assert_not_called()
    mock_artefact.assert_called_once()


@patch("letxbe.main.Artefact.parse_obj")
@patch("letxbe.main.Target.parse_obj")
@patch("letxbe.main.requests.get")
def test_lxb__get_document__target(mock_get, mock_target, mock_artefact, mock_lxb):
    # Given
    mock_get.return_value = Mock(
        json=lambda: {"some_key": "some_value"}, status_code=200
    )
    automatisme_slug = "atms-slug"
    document_slug = "target-slug"

    # When
    mock_lxb.get_document(automatisme_slug, document_slug)

    # Then
    mock_target.assert_called_once()
    mock_artefact.assert_not_called()


@pytest.mark.parametrize("file", [bytes(secrets.randbelow(16)), None])
@patch("letxbe.main.requests.post")
def test_lxb___post_document(mock_post, mock_lxb, file):
    # Given
    mock_post.return_value = Mock(text="", status_code=200)
    route = Mock()
    metadata = Metadata(
        name="Random number sent as file bytes",
        artefact={},
    )

    # When
    mock_lxb._post_document(route, metadata, file)

    # Then
    mock_post.assert_called_once()
