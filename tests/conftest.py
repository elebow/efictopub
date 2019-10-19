import inspect
import os
import pytest
import requests

from pytest_factoryboy import register

from efictopub import config

import efictopub.lib.reddit_util
import efictopub.lib.request_dispatcher


# requests

if os.environ.get("LIVE_REQUESTS") != "true":

    @pytest.fixture(autouse=True, scope="session")
    def no_reddit():
        from unittest.mock import MagicMock

        efictopub.lib.reddit_util.setup_reddit = MagicMock()

    efictopub.lib.request_dispatcher.MIN_DELAY = 0


# config

config.load({}, fetcher=None)


# fixtures and factories

import factory
from tests import factories

# register all of the factory.Factory subclasses in tests.factories
for (name, factory_class) in inspect.getmembers(factories):
    if inspect.isclass(factory_class) and issubclass(factory_class, factory.Factory):
        register(factory_class)

from tests.fixtures.real import redditor_with_submissions, praw_comment, praw_submission
