from unittest.mock import MagicMock
from unittest.mock import patch

from efictopub.efictopub import Efictopub


@patch("efictopub.efictopub.Efictopub.fetch_story", MagicMock())
class TestEfictopub:
    @patch("efictopub.efictopub.Efictopub.get_fetcher", MagicMock())
    @patch("efictopub.efictopub.Efictopub.check_repo_ready_for_write", lambda _x: True)
    @patch("efictopub.archive.store")
    @patch("efictopub.git.previous_commit_is_not_efic")
    def test_archive_story(self, archive_store, previous_commit_not_efic):
        efictopub = Efictopub()
        efictopub.archive_story()

        archive_store.assert_called_once()
        previous_commit_not_efic.assert_called_once()

    @patch("efictopub.efictopub.Efictopub.check_repo_ready_for_write", lambda _x: True)
    @patch("efictopub.fetchers.fetcher_by_name")
    def test_get_fetcher_manual(self, fetcher_by_name):
        Efictopub({"target": "www.example.com/great-story", "fetcher": "reddit_next"})

        fetcher_by_name.assert_called_once_with(
            "reddit_next", "www.example.com/great-story"
        )

    @patch("efictopub.efictopub.Efictopub.check_repo_ready_for_write", lambda _x: True)
    @patch("efictopub.fetchers.fetcher_for_url")
    def test_get_fetcher_auto(self, fetcher_for_url):
        Efictopub({"target": "www.example.com/great-story"})

        fetcher_for_url.assert_called_once_with("www.example.com/great-story")

    @patch("efictopub.git.repo_is_dirty", lambda: False)
    @patch("efictopub.efictopub.Efictopub.get_fetcher", MagicMock())
    def test_check_repo_ready_for_write_repo_clean(self):
        efictopub = Efictopub({"write_archive": True, "clobber": False})

        assert efictopub.check_repo_ready_for_write() is True

    @patch("efictopub.git.repo_is_dirty", lambda: True)
    @patch("efictopub.efictopub.Efictopub.get_fetcher", MagicMock())
    def test_check_repo_ready_for_write_repo_dirty(self):
        efictopub = Efictopub({"write_archive": True, "clobber": False})

        assert efictopub.check_repo_ready_for_write() is False

    @patch("efictopub.git.repo_is_dirty", lambda: True)
    @patch("efictopub.efictopub.Efictopub.get_fetcher", MagicMock())
    def test_check_repo_ready_for_write_repo_dirty_no_write(self):
        efictopub = Efictopub({"write_archive": False, "clobber": False})

        assert efictopub.check_repo_ready_for_write() is True

    @patch("efictopub.git.repo_is_dirty", lambda: True)
    @patch("efictopub.efictopub.Efictopub.get_fetcher", MagicMock())
    def test_check_repo_ready_for_write_repo_dirty_clobber(self):
        efictopub = Efictopub({"write_archive": True, "clobber": True})

        assert efictopub.check_repo_ready_for_write() is True
