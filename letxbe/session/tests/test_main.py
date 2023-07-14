import secrets
from unittest.mock import Mock, patch

import pytest
from requests import Response

from letxbe.session import LXBSession


@pytest.fixture(scope="session")
def mock_lxbsession(mock_access_token) -> LXBSession:
    with patch(
        "letxbe.session.main.requests.post",
        return_value=Mock(
            status_code=201, json=lambda: {"access_token": mock_access_token}
        ),
    ):
        lxbsession = LXBSession("", "")
    return lxbsession


@pytest.mark.parametrize("status_code", [403, 404, 500])
def test__verify_status_code__raise_error(mock_lxbsession, status_code):
    # Given
    resp = Response()
    resp.status_code = status_code

    # Then
    with pytest.raises(Exception):
        mock_lxbsession._verify_status_code(resp)


def test__verify_status_code_success(mock_lxbsession):
    # Given
    resp = Response()
    resp.status_code = secrets.randbelow(200)

    # Then
    with pytest.raises(ValueError) as exc_info:
        mock_lxbsession._verify_status_code(resp)

    assert f"Request failed with code {resp.status_code}" in str(exc_info.value)


def test_authorization_header(mock_lxbsession, mock_access_token):
    # Then
    assert (
        mock_lxbsession.authorization_header["Authorization"]
        == "Bearer " + mock_access_token
    )
