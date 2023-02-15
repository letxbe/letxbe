import pytest


@pytest.fixture(scope="session")
def mock_access_token() -> str:
    return "some_access_token"
