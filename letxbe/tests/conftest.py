import os
import warnings

import pytest

from letxbe import LXB

CLIENT_ID = os.environ.get("CLIENT_ID", None)
CLIENT_SECRET = os.environ.get("CLIENT_SECRET", None)
BASE_URL = "https://staging-unfold.onogone.com"


@pytest.fixture
def lxb():
    if CLIENT_ID is None or CLIENT_SECRET is None:
        warnings.warn(UserWarning("no credentials provided, sandbox tests cannot run."))
        return

    return LXB(CLIENT_ID, CLIENT_SECRET, BASE_URL)
