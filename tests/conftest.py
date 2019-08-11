import os
import pytest
import requests

from unittest.mock import MagicMock

from app import config

import app.lib.reddit_util
import app.lib.request_delay
import tests.fixtures.stubs


if os.environ.get("LIVE_REQUESTS") != "true":

    @pytest.fixture(autouse=True, scope="session")
    def no_reddit():
        app.lib.reddit_util.setup_reddit = MagicMock()

    @pytest.fixture(autouse=True, scope="session")
    def no_requests():
        requests.get = tests.fixtures.stubs.request_get

    app.lib.request_delay.MIN_DELAY = 0


def load_config_file():
    import confuse

    conf = confuse.Configuration("efictopub", read=False)
    conf.set_file("tests/fixtures/config.yaml")
    return conf


config.load_config_file = load_config_file
config.load(args={}, fetcher=None)
