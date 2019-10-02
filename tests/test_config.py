import pytest
from unittest.mock import MagicMock
from unittest.mock import patch

from app import config


def configparser_get(section, key, fallback=None):
    return {
        "REDDIT": {
            "app": "my-great-app",
            "secret": "top-secret",
            "user_agent": "my-great-user-agent"
        },
        "ARCHIVE": {
            "location": "my-great-location"
        }
    }[section][key]


@pytest.fixture
def configparser():
    return MagicMock(get=configparser_get)


class TestConfig:

    @patch("configparser.ConfigParser", configparser)
    def setup_method(self, configparser):
        config.load("_whatever.ini")  # re-load with our stubbed ConfigParser

    def teardown(self):
        config.load("config.ini")  #TODO

    def test_reddit(self):
        assert dict(config.reddit._asdict()) == {"app": "my-great-app",
                                                 "secret": "top-secret",
                                                 "user_agent": "my-great-user-agent"}

    def test_archive(self):
        assert dict(config.archive._asdict()) == {"location": "my-great-location"}
