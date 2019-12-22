import pytest

from efictopub import config
from efictopub.fetchers import spacebattles

from tests.fixtures import spacebattles_threadmarks_index_html
from tests.fixtures import spacebattles_thread_reader_1_html
from tests.fixtures import spacebattles_thread_reader_2_html


class TestFetchersSpacebattles:
    @pytest.fixture
    def generate_posts(self, mocker):
        def posts(_self, category):
            if category == "threadmarks":
                return [
                    mocker.MagicMock(text="threadmark 1", date_published=10),
                    mocker.MagicMock(text="threadmark 2", date_published=20),
                    mocker.MagicMock(text="threadmark 3", date_published=30),
                ]
            elif category == "sidestory":
                return [
                    mocker.MagicMock(text="sidestory 1", date_published=11),
                    mocker.MagicMock(text="sidestory 2", date_published=26),
                ]
            elif category == "announcement":
                return [mocker.MagicMock(text="announcement 1", date_published=15)]
            else:
                raise  # this means a test is broken

        mocker.patch(
            "efictopub.fetchers.spacebattles.Fetcher.generate_threadmarked_posts", posts
        )

    @pytest.fixture
    def threadmarks_categories(self, mocker):
        mocker.patch(
            "efictopub.fetchers.spacebattles.Fetcher.threadmarks_categories",
            {"threadmarks": "1", "sidestory": "2", "announcement": "3"},
        )

    @pytest.fixture(autouse=True)
    def base_config(self):
        config.config["fetcher_opts"] = ["title=Great Story"]

    def test_fetch_story(self, requests_mock):
        requests_mock.get(
            "https://forums.spacebattles.com/threads/555/threadmarks?category_id=1",
            text=spacebattles_threadmarks_index_html,
        )
        requests_mock.get(
            "https://forums.spacebattles.com/threads/555/1/reader/",
            text=spacebattles_thread_reader_1_html,
        )
        requests_mock.get(
            "https://forums.spacebattles.com/threads/my-great-story.555/reader/page-2",
            text=spacebattles_thread_reader_2_html,
        )

        fetcher = spacebattles.Fetcher("https://forums.spacebattles.com/threads/555/")
        story = fetcher.fetch_story()
        chapter_0 = story.chapters[0]

        assert story.author == "User 1"
        assert chapter_0.date_published == 1522580101
        assert chapter_0.date_updated == 0
        assert (
            chapter_0.permalink
            == "https://forums.spacebattles.com/threads/my-great-story.555/post-500"
        )
        assert chapter_0.score == 173
        assert chapter_0.text == "post 1 content"
        assert chapter_0.title == "threadmark description 771"

        assert story.chapters[1].date_updated == 1561568837

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

    def test_threadmarks_categories(self, requests_mock):
        requests_mock.get(
            "https://forums.spacebattles.com/threads/555/threadmarks?category_id=1",
            text=spacebattles_threadmarks_index_html,
        )

        fetcher = spacebattles.Fetcher("https://forums.spacebattles.com/threads/555/")
        assert fetcher.threadmarks_categories == {
            "threadmarks": "1",
            "sidestory": "19",
            "informational": "19",
            "staff post": "7",
        }

    def test_categories_and_order_default(self, generate_posts, threadmarks_categories):
        fetcher = spacebattles.Fetcher("https://forums.spacebattles.com/threads/555/")
        posts = fetcher.fetch_posts()

        assert [post.text for post in posts] == [
            "threadmark 1",
            "threadmark 2",
            "threadmark 3",
        ]

    def test_categories_and_order_two_categories(
        self, generate_posts, threadmarks_categories
    ):
        config.config["fetcher_opts"] = ["categories=threadmarks,sidestory"]

        fetcher = spacebattles.Fetcher("https://forums.spacebattles.com/threads/555/")
        posts = fetcher.fetch_posts()

        assert [post.text for post in posts] == [
            "threadmark 1",
            "threadmark 2",
            "threadmark 3",
            "sidestory 1",
            "sidestory 2",
        ]

    def test_categories_and_order_all(self, generate_posts, threadmarks_categories):
        config.config["fetcher_opts"] = ["categories=all"]

        fetcher = spacebattles.Fetcher("https://forums.spacebattles.com/threads/555/")
        posts = fetcher.fetch_posts()

        assert [post.text for post in posts] == [
            "threadmark 1",
            "threadmark 2",
            "threadmark 3",
            "sidestory 1",
            "sidestory 2",
            "announcement 1",
        ]

    def test_categories_and_order_all_chrono(
        self, generate_posts, threadmarks_categories
    ):
        config.config["fetcher_opts"] = ["categories=all", "order=chrono"]

        fetcher = spacebattles.Fetcher("https://forums.spacebattles.com/threads/555/")
        posts = fetcher.fetch_posts()

        assert [post.text for post in posts] == [
            "threadmark 1",
            "sidestory 1",
            "announcement 1",
            "threadmark 2",
            "sidestory 2",
            "threadmark 3",
        ]
