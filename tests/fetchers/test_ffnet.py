from unittest.mock import MagicMock

from app.fetchers.ffnet import FFNet

from tests.fixtures.real import ffnet_chapter_html_real
from tests.fixtures.real import ffnet_chapter_2_html_real
from tests.fixtures.real import ffnet_chapter_3_html_real
from tests.fixtures.real import ffnet_single_chapter_story_html_real
from tests.fixtures.real import ffnet_single_chapter_story_reviews_html_real
import tests.fixtures.stubs


class TestFetchersFFNet:
    def test_fetch_story(self):
        tests.fixtures.stubs.return_values = [
            MagicMock(status_code=200, text=ffnet_chapter_html_real()),
            MagicMock(status_code=200, text="reviews for chapter 1"),

            MagicMock(status_code=200, text=ffnet_chapter_2_html_real()),
            MagicMock(status_code=200, text="reviews for chapter 2"),

            MagicMock(status_code=200, text=ffnet_chapter_3_html_real()),
            MagicMock(status_code=200, text="reviews for chapter 3")
        ]
        fetcher = FFNet("https://www.fanfiction.net/s/555/8/")
        story = fetcher.fetch_story()
        assert story.title == "My Great Story"
        assert story.chapters[0].title == "1. Yes, these option tags are"
        assert [ch.text for ch in story.chapters] == [
            "Story Text *Goes* **Here**. Chapter 1.",
            "Story Text *Goes* **Here**. Chapter 2.",
            "Story Text *Goes* **Here**. Chapter 3."
        ]
        assert [ch.comments for ch in story.chapters] == [
            "reviews for chapter 1",
            "reviews for chapter 2",
            "reviews for chapter 3"
        ]

    """
    def test_generate_chapters(self):
        tests.fixtures.stubs.return_values = [
            MagicMock(status_code=200, text="5"),
            MagicMock(status_code=200, text="6"),
            MagicMock(status_code=200, text="7"),
            MagicMock(status_code=200, text="FanFiction.Net Message Type 1<hr size=1 noshade>Chapter not found.")
        ]
        fetcher = FFNet("https://www.fanfiction.net/s/555/8/")
        htmls = [x for x in fetcher.generate_ffnet_chapters()]
        assert htmls == ["5", "6", "7"]
    """

    def test_generate_chapters_for_single_chapter_story(self):
        tests.fixtures.stubs.return_values = [
            MagicMock(status_code=200, text=ffnet_single_chapter_story_html_real()),
            MagicMock(status_code=200, text=ffnet_single_chapter_story_reviews_html_real())
        ]
        fetcher = FFNet("https://www.fanfiction.net/s/555/8/")
        htmls = [x for x in fetcher.generate_ffnet_chapters()]
        assert len(htmls) == 1
        assert htmls[0].text == "Story Text *Goes* **Here**."

    def test_calculate_ffnet_id(self):
        assert FFNet("https://www.fanfiction.net/s/555/8/").ffnet_id == "555"
        assert FFNet("https://www.fanfiction.net/s/555/2/My-Great-Story").ffnet_id == "555"
        assert FFNet("111").ffnet_id == "111"
        assert FFNet("a").ffnet_id == None
