import os
import pytest
import requests

from unittest.mock import MagicMock

from app import config_loader
import app


def load_config_file():
    import confuse

    conf = confuse.Configuration("efictopub", read=False)
    conf.set_file("tests/fixtures/config.yaml")
    return conf


app.config_loader.load_config_file = load_config_file
app.config_loader.load(args={}, fetcher=None)


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

    app.lib.request_delay.DELAY = 0
