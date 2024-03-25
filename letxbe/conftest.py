from unittest.mock import Mock, patch

import pytest
import requests

from letxbe.main import LXB


class MockSession:
    def post(self, **kwargs) -> requests.Response:
        response = requests.Response()
        response.json = Mock(return_value={})
        response.status_code = 200
        return response

    def get(self, **kwargs):
        return self.post()


@pytest.fixture(scope="session")
def mock_access_token() -> str:
    return "some_access_token"


@pytest.fixture
def mock_lxb__mocked_session():
    with patch(
        "letxbe.main.create_letxbe_session",
        return_value=MockSession(),
    ):
        lxb = LXB("client_id", "client_secret")
    return lxb


@pytest.fixture
def mock_lxb():
    with patch(
        "letxbe.main.create_letxbe_session",
        return_value=requests.Session(),
    ):
        lxb = LXB("client_id", "client_secret")
    return lxb
