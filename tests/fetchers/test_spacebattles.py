from unittest.mock import MagicMock

from efictopub import config
from efictopub.fetchers import spacebattles

from tests.fixtures.real import spacebattles_threadmarks_index_html
from tests.fixtures.real import spacebattles_thread_reader_1_html
from tests.fixtures.real import spacebattles_thread_reader_2_html
from tests.fixtures.stubs import stub_response


class TestFetchersSpacebattles:
    def setup_method(self):
        config.config["fetcher_opts"] = ["title=Great Story"]

    def test_threadmark_category(self):
        # TODO only assert that generate_threadmarked_posts() is called with the right args
        pass

    def test_fetch_story(self):
        stub_response(spacebattles_thread_reader_1_html)
        stub_response(spacebattles_thread_reader_2_html)

        fetcher = spacebattles.Fetcher("https://forums.spacebattles.com/threads/555/")
        story = fetcher.fetch_story()
        chapter_0 = story.chapters[0]

        assert story.author == "user1"
        assert chapter_0.date_published == 1407771960
        assert chapter_0.date_updated == 1542691740
        assert chapter_0.permalink == "https://forums.spacebattles.com/posts/55520034/"
        assert chapter_0.score == 120
        assert chapter_0.text == "post 1 content"
        assert chapter_0.title == "threadmark description 771"

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
        stub_response(spacebattles_threadmarks_index_html)

        fetcher = spacebattles.Fetcher("https://forums.spacebattles.com/threads/555/")
        assert fetcher.threadmarks_categories == {
            "threadmarks": "1",
            "sidestory": "16",
            "apocrypha": "13",
            "media": "10",
            "informational": "19",
        }
