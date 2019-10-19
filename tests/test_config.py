from efictopub import config


test_config = {
    "reddit": {"app": "app-id", "secret": "app-secret"},
    "archive_location": "/path/to/archive",
    "epub_location": "$HOME/books/fic/",
    "fetch_comments": True,
    "write_archive": True,
    "write_epub": True,
    "overrides": {
        "reddit_next": {
            "epub_location": "$HOME/doc/books/reddit_fics/",
            "write_epub": False,
            "reddit": {"app": "reddit-next-app-id"},
        },
        "ffnet": {"fetch_comments": False},
    },
}


class TestConfig:
    @classmethod
    def teardown_class(_cls):
        config.load(test_config, fetcher=None)

    def test_load(self):
        config.load(test_config, fetcher=None)

        assert config.get("archive_location") == "/path/to/archive"
        assert config.get("fetch_comments") is True

    def test_fetcher_overrides(self, mocker):
        config.load(test_config, fetcher=mocker.MagicMock(__module__="reddit_next"))

        assert config.get("write_epub") is False
        assert config.get(["reddit", "app"]) == "reddit-next-app-id"

    def test_nonexistent_fetcher_override(self, mocker):
        config.load(test_config, fetcher=mocker.MagicMock(__module__="rabbits"))

        assert config.get("fetch_comments") is True

    def test_get_fetcher_opt(self, mocker):
        config.load(
            {"fetcher_opts": ["a=5", "ab=6"]},
            fetcher=mocker.MagicMock(__module__="reddit_next"),
        )

        assert config.get_fetcher_opt("a") == "5"
        assert config.get_fetcher_opt("ab") == "6"
