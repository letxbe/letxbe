import pytest
from dotenv import load_dotenv

load_dotenv()


@pytest.fixture(scope="session")
def mock_access_token() -> str:
    return "some_access_token"
