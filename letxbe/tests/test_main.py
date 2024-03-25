import secrets
from unittest.mock import Mock, patch

import pytest
from requests import Response

from letxbe.exception import UnauthorizedError
from letxbe.main import LXB
from letxbe.type import Metadata


@patch("letxbe.main.requests.post")
def test_lxb__auth_error(mocked_post):
    # Given
    mocked_post.return_value = Mock(status_code=401)
    client_id = "asbadf"
    client_secret = "akjhb"

    # Then
    with pytest.raises(UnauthorizedError):
        LXB(client_id, client_secret)


@patch("letxbe.main.Artefact.parse_obj")
@patch("letxbe.main.Target.parse_obj")
def test_lxb__get_document__target(
    mock_target, mock_artefact, mock_lxb__mocked_session
):
    # Given
    automatisme_slug = "atms-slug"
    document_slug = "target-slug"

    # When
    mock_lxb__mocked_session.get_document(automatisme_slug, document_slug)

    # Then
    mock_target.assert_called_once()
    mock_artefact.assert_not_called()


@pytest.mark.parametrize("file", [bytes(secrets.randbelow(16)), None])
@patch("letxbe.main.LXB._verify_status_code")
def test_lxb___post_document(mock__verify_status_code, mock_lxb__mocked_session, file):
    # Given
    route = "https://some_route"
    metadata = Metadata(
        name="Random number sent as file bytes",
        artefact={},
    )

    # When
    response = mock_lxb__mocked_session._post_document(route, metadata, file)

    # Then
    mock__verify_status_code.assert_called_once()
    assert response == {}


@pytest.mark.parametrize("status_code", [403, 404, 500])
def test_lxb___verify_status_code__raise_error(mock_lxb, status_code):
    # Given
    resp = Response()
    resp.status_code = status_code

    # Then
    with pytest.raises(Exception):
        mock_lxb._verify_status_code(resp)


def test_lxb___verify_status_code_success(mock_lxb):
    # Given
    resp = Response()
    resp.status_code = secrets.randbelow(200)

    # Then
    with pytest.raises(ValueError) as exc_info:
        mock_lxb._verify_status_code(resp)

    assert f"Request failed with code {resp.status_code}" in str(exc_info.value)
