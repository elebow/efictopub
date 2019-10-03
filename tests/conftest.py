import os
import pytest
import requests

from unittest.mock import MagicMock

from efictopub import config

import efictopub.lib.reddit_util
import efictopub.lib.request_dispatcher
import tests.fixtures.stubs


if os.environ.get("LIVE_REQUESTS") != "true":

    @pytest.fixture(autouse=True, scope="session")
    def no_reddit():
        efictopub.lib.reddit_util.setup_reddit = MagicMock()

    @pytest.fixture(autouse=True, scope="session")
    def no_requests():
        requests.get = tests.fixtures.stubs.request_get

    efictopub.lib.request_dispatcher.MIN_DELAY = 0


@pytest.fixture(autouse=True, scope="function")
def empty_stubbed_responses():
    yield

    num_leftover_stubbed_responses = len(tests.fixtures.stubs.responses)

    # reset the responses so later functions can still pass, if the follower assertion fails
    tests.fixtures.stubs.responses = []

    # ensure stubbed http responses are all used up at the end of every case
    assert num_leftover_stubbed_responses == 0


def load_config_file():
    import confuse

    conf = confuse.Configuration("efictopub", read=False)
    conf.set_file("tests/fixtures/config.yaml")
    return conf


config.load_config_file = load_config_file
config.load(args={}, fetcher=None)
