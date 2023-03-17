import pytest
from dotenv import load_dotenv

# Why are we using load_dotenv here instead of pytest-env and a pytest.ini? Especially since there is no `.env` to use?
load_dotenv()


@pytest.fixture(scope="session")
def mock_access_token() -> str:
    return "some_access_token"
