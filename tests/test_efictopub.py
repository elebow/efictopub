import confuse
import pytest

from efictopub.efictopub import Efictopub


class TestEfictopub:
    @pytest.fixture(autouse=True)
    def fetch_story(self, mocker):
        mocker.patch("efictopub.efictopub.Efictopub.fetch_story")

    @pytest.fixture
    def load_config_file(self, mocker):
        conf = confuse.Configuration("efictopub", read=False)
        conf.set_file("tests/fixtures/config.yaml")
        mocker.patch("confuse.Configuration", lambda _x, _y: conf)

    def test_load_config(self, mocker, load_config_file):
        efictopub = Efictopub(
            {
                "target": "www.fanfiction.net/great-story",
                "comments": "author",
                "write_epub": False,
            }
        )

        # defaults from the test fixture config.yaml
        assert efictopub.opts["archive_location"] == "/path/to/archive"

        # CLI overrides
        assert efictopub.opts["write_epub"] is False

        # fetcher overrides
        assert efictopub.opts["epub_location"] == "/some/other/epub/location"

        # CLI options take precedence over the config file's fetcher_overrides
        assert efictopub.opts["comments"] == "author"

    def test_archive_story(self, mocker):
        mocker.patch("efictopub.efictopub.Efictopub.get_fetcher")
        mocker.patch(
            "efictopub.efictopub.Efictopub.repo_ready_for_write", lambda _x: True
        )
        archive_store = mocker.patch("efictopub.archive.store")
        previous_commit_not_efic = mocker.patch(
            "efictopub.git.previous_commit_is_not_efic"
        )

        Efictopub().archive_story()

        archive_store.assert_called_once()
        previous_commit_not_efic.assert_called_once()

    def test_get_fetcher_manual(self, mocker):
        mocker.patch(
            "efictopub.efictopub.Efictopub.repo_ready_for_write", lambda _x: True
        )
        fetcher_by_name = mocker.patch("efictopub.fetchers.fetcher_by_name")

        Efictopub({"target": "www.example.com/great-story", "fetcher": "reddit_next"})

        fetcher_by_name.assert_called_once_with(
            "reddit_next", "www.example.com/great-story"
        )

    def test_get_fetcher_auto(self, mocker):
        mocker.patch(
            "efictopub.efictopub.Efictopub.repo_ready_for_write", lambda _x: True
        )
        fetcher_for_url = mocker.patch("efictopub.fetchers.fetcher_for_url")

        Efictopub({"target": "www.example.com/great-story"})

        fetcher_for_url.assert_called_once_with("www.example.com/great-story")

    def test_repo_ready_for_write_repo_clean(self, mocker):
        mocker.patch("efictopub.git.repo_is_dirty", lambda: False)
        mocker.patch("efictopub.efictopub.Efictopub.get_fetcher")

        efictopub = Efictopub({"write_archive": True, "clobber": False})

        assert efictopub.repo_ready_for_write() is True

    def test_repo_ready_for_write_repo_dirty(self, mocker):
        mocker.patch("efictopub.git.repo_is_dirty", lambda: True)
        mocker.patch("efictopub.efictopub.Efictopub.get_fetcher")

        efictopub = Efictopub({"write_archive": True, "clobber": False})

        assert efictopub.repo_ready_for_write() is False

    def test_repo_ready_for_write_repo_dirty_no_write(self, mocker):
        mocker.patch("efictopub.git.repo_is_dirty", lambda: True)
        mocker.patch("efictopub.efictopub.Efictopub.get_fetcher")

        efictopub = Efictopub({"write_archive": False, "clobber": False})

        assert efictopub.repo_ready_for_write() is True

    def test_repo_ready_for_write_repo_dirty_clobber(self, mocker):
        mocker.patch("efictopub.git.repo_is_dirty", lambda: True)
        mocker.patch("efictopub.efictopub.Efictopub.get_fetcher")

        efictopub = Efictopub({"write_archive": True, "clobber": True})

        assert efictopub.repo_ready_for_write() is True
