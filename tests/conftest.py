import confuse
import inspect
import os
import pytest
import requests

from pytest_factoryboy import register

from efictopub import config

import efictopub.lib.reddit_util
import efictopub.lib.request_dispatcher


# requests


@pytest.fixture(autouse=True, scope="session")
def no_reddit():
    from unittest.mock import MagicMock

    efictopub.lib.reddit_util.setup_reddit = MagicMock()


efictopub.lib.request_dispatcher.MIN_DELAY = 0


# config


@pytest.fixture(autouse=True)
def load_config_file(mocker):
    conf = confuse.Configuration("efictopub", read=False)
    conf.set_file("tests/fixtures/config.yaml")
    mocker.patch("confuse.Configuration", lambda _x, _y: conf)


# fixtures and factories

import factory
from tests import factories

# register all of the factory.Factory subclasses in tests.factories
for (name, factory_class) in inspect.getmembers(factories):
    if inspect.isclass(factory_class) and issubclass(factory_class, factory.Factory):
        register(factory_class)

from tests.fixtures import redditor_with_submissions, praw_comment, praw_submission
