from unittest.mock import MagicMock
from unittest.mock import patch

import argparse
import confuse

from app import config_loader


def load_config_file():
    conf = confuse.Configuration("efictopub", read=False)
    conf.set_file("tests/fixtures/config.yaml")
    return conf


class TestConfig:
    @patch("app.config_loader.load_config_file", load_config_file)
    def test_load_file(self):
        config_loader.load(args={}, fetcher=None)
        from app import config

        assert config["archive_location"].get() == "/path/to/archive"
        assert config["fetch_comments"].get(bool) is True

    @patch("app.config_loader.load_config_file", load_config_file)
    def test_fetcher_overrides(self):
        config_loader.load(args={}, fetcher=MagicMock(__module__="reddit_next"))
        from app import config

        assert config["write_epub"].get(bool) is False
        assert config["reddit"]["app"].get() == "reddit-next-app-id"

    @patch("app.config_loader.load_config_file", load_config_file)
    def test_nonexistent_fetcher_override(self):
        config_loader.load(args={}, fetcher=MagicMock(__module__="rabbits"))
        from app import config

        assert config["fetch_comments"].get(bool) is True

    @patch("app.config_loader.load_config_file", load_config_file)
    def test_cli_arg_overrides(self):
        arg_parser = argparse.ArgumentParser()
        arg_parser.add_argument("--reddit.app", type=str)
        args = arg_parser.parse_args(["--reddit.app=other-app-id"])

        config_loader.load(args=args, fetcher=MagicMock(__module__="rabbits"))
        from app import config

        assert config["reddit"]["app"].get() == "other-app-id"

    @patch("app.config_loader.load_config_file", load_config_file)
    def test_cli_arg_and_fetcher_overrides(self):
        arg_parser = argparse.ArgumentParser()
        arg_parser.add_argument("--fetch_comments", type=str)
        args = arg_parser.parse_args(["--fetch_comments=5"])

        config_loader.load(args=args, fetcher=MagicMock(__module__="ffnet"))
        from app import config

        assert config["fetch_comments"].get() == "5"
