from efictopub import config


test_config = {
    "reddit": {"app": "app-id", "secret": "app-secret"},
    "archive_location": "/path/to/archive",
    "epub_location": "$HOME/books/fic/",
    "comments": "all",
    "write_archive": True,
    "write_epub": True,
    "overrides": {
        "reddit_next": {
            "epub_location": "$HOME/doc/books/reddit_fics/",
            "write_epub": False,
            "reddit": {"app": "reddit-next-app-id"},
        },
        "ffnet": {"comments": "none"},
    },
}


class TestConfig:
    @classmethod
    def teardown_class(_cls):
        config.load(test_config, fetcher=None)

    def test_load(self):
        config.load(test_config, fetcher=None)

        assert config.get("archive_location") == "/path/to/archive"
        assert config.get("comments") == "all"

    def test_nonexistent_fetcher_override(self, mocker):
        config.load(test_config, fetcher=mocker.MagicMock(__module__="rabbits"))

        assert config.get("comments") == "all"

    def test_get_fetcher_opt(self, mocker):
        config.load(
            {"fetcher_opts": ["a=5", "ab=6"]},
            fetcher=mocker.MagicMock(__module__="reddit_next"),
        )

        assert config.get_fetcher_opt("a") == "5"
        assert config.get_fetcher_opt("ab") == "6"
