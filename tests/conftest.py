import os
import pytest
import requests
from unittest.mock import MagicMock

import app.lib.reddit_util
import tests.fixtures.stubs

if os.environ.get("LIVE_REQUESTS") != "true":
    @pytest.fixture(autouse=True, scope="session")
    def no_reddit():
        app.lib.reddit_util.setup_reddit = MagicMock()

    @pytest.fixture(autouse=True, scope="session")
    def no_requests():
        requests.get = tests.fixtures.stubs.request_get
