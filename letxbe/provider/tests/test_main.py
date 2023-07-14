from unittest.mock import Mock, patch

import pytest
from requests import Response

from letxbe.exception import AutomationError
from letxbe.provider import Provider


@pytest.fixture(scope="session")
def mock_provider_urn() -> str:
    return "some provider urn"


@pytest.fixture(scope="session")
def mock_provider(mock_access_token, mock_provider_urn) -> Provider:
    with patch(
        "letxbe.session.main.requests.post",
        return_value=Mock(
            status_code=201, json=lambda: {"access_token": mock_access_token}
        ),
    ):
        provider = Provider(
            client_id="", client_secret="", provider_urn=mock_provider_urn
        )

    assert provider.urn == mock_provider_urn
    return provider


def test__verify_response_is_success__raise_error(mock_provider):
    # Given
    resp = Response()
    resp.status_code = 200

    resp.json = lambda: '{"status": "failed"}'

    # Then
    with pytest.raises(AutomationError):
        mock_provider._verify_response_is_success(resp)


def test__verify_response_is_success(mock_provider):
    # Given
    resp = Response()
    resp.status_code = 200
    resp.json = lambda: '{"status": "success"}'

    # Then
    assert mock_provider._verify_response_is_success(resp) is None


def test_authorization_header(mock_provider, mock_access_token):
    # Then
    assert (
        mock_provider.authorization_header["Authorization"]
        == "Bearer " + mock_access_token
    )


def test_save__raise_error_if_bytes(mock_provider):
    # Given
    mock_input = (b"", b"")
    mock_slug = Mock()

    # Then
    with pytest.raises(NotImplementedError):
        mock_provider.save_and_finish(task_slug=mock_slug, data=mock_input)
