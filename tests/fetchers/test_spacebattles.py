from unittest.mock import MagicMock

from efictopub import config
from efictopub.fetchers import spacebattles

from tests.fixtures.real import spacebattles_threadmarks_index_html_real
from tests.fixtures.stubs import stub_response


class TestFetchersSpacebattles:
    def test_calculate_thread_id(self):
        def get_id(x):
            return spacebattles.Fetcher(x).thread_id

        assert (
            get_id(
                "https://forums.spacebattles.com/threads/555/threadmarks?category_id=1"
            )
            == "555"
        )
        assert get_id("https://forums.spacebattles.com/threads/555/") == "555"
        assert get_id("https://forums.spacebattles.com/threads/555") == "555"
        assert (
            get_id("https://forums.spacebattles.com/threads/my-great-story.555/")
            == "555"
        )
        assert get_id("111") == "111"
        assert get_id("a") is None

    def test_threadmarks_categories(self):
        stub_response(spacebattles_threadmarks_index_html_real)

        fetcher = spacebattles.Fetcher("https://forums.spacebattles.com/threads/555/")
        assert fetcher.threadmarks_categories == {
            "threadmarks": "1",
            "sidestory": "16",
            "apocrypha": "13",
            "media": "10",
            "informational": "19",
        }
