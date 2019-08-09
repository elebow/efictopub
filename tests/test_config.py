from unittest.mock import MagicMock
from unittest.mock import patch

import argparse
import confuse

from app import config


def load_config_file():
    conf = confuse.Configuration("efictopub", read=False)
    conf.set_file("tests/fixtures/config.yaml")
    return conf


class TestConfig:
    @classmethod
    def teardown_class(_cls):
        config.load(args={}, fetcher=None)

    @patch("app.config.load_config_file", load_config_file)
    def test_load_file(self):
        config.load(args={}, fetcher=None)

        assert config.get("archive_location") == "/path/to/archive"
        assert config.get("fetch_comments", bool) is True

    @patch("app.config.load_config_file", load_config_file)
    def test_fetcher_overrides(self):
        config.load(args={}, fetcher=MagicMock(__module__="reddit_next"))

        assert config.get("write_epub", bool) is False
        assert config.get(["reddit", "app"]) == "reddit-next-app-id"

    @patch("app.config.load_config_file", load_config_file)
    def test_nonexistent_fetcher_override(self):
        config.load(args={}, fetcher=MagicMock(__module__="rabbits"))

        assert config.get("fetch_comments", bool) is True

    @patch("app.config.load_config_file", load_config_file)
    def test_cli_arg_overrides(self):
        arg_parser = argparse.ArgumentParser()
        arg_parser.add_argument("--reddit.app", type=str)
        args = arg_parser.parse_args(["--reddit.app=other-app-id"])

        config.load(args=args, fetcher=MagicMock(__module__="rabbits"))

        assert config.get(["reddit", "app"]) == "other-app-id"

    @patch("app.config.load_config_file", load_config_file)
    def test_cli_arg_and_fetcher_overrides(self):
        arg_parser = argparse.ArgumentParser()
        arg_parser.add_argument("--fetch_comments", type=str)
        args = arg_parser.parse_args(["--fetch_comments=5"])

        config.load(args=args, fetcher=MagicMock(__module__="ffnet"))

        assert config.get("fetch_comments") == "5"
