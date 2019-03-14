from unittest.mock import MagicMock

from app.fetchers import ffnet

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
        fetcher = ffnet.Fetcher("https://www.fanfiction.net/s/555/8/")
        story = fetcher.fetch_story()
        assert story.title == "My Great Story"
        assert story.chapters[0].title == "1. Yes, these option tags are"
        assert [ch.text for ch in story.chapters] == [
            "<p>\n    Story Text <em>Goes</em> <strong>Here</strong>. Chapter 1.\n    </p>",
            "<p>\n    Story Text <em>Goes</em> <strong>Here</strong>. Chapter 2.\n    </p>",
            "<p>\n    Story Text <em>Goes</em> <strong>Here</strong>. Chapter 3.\n    </p>",
        ]
        assert [ch.comments for ch in story.chapters] == [
            "reviews for chapter 1",
            "reviews for chapter 2",
            "reviews for chapter 3"
        ]

    def test_generate_chapters_for_single_chapter_story(self):
        tests.fixtures.stubs.return_values = [
            MagicMock(status_code=200, text=ffnet_single_chapter_story_html_real()),
            MagicMock(status_code=200, text=ffnet_single_chapter_story_reviews_html_real())
        ]
        fetcher = ffnet.Fetcher("https://www.fanfiction.net/s/555/8/")
        htmls = [x for x in fetcher.generate_ffnet_chapters()]
        assert len(htmls) == 1
        assert htmls[0].text == "<p>\n       Story Text <em>Goes</em> <strong>Here</strong>.\n       </p>"

    def test_calculate_ffnet_id(self):
        assert ffnet.Fetcher("https://www.fanfiction.net/s/555/8/").ffnet_id == "555"
        assert ffnet.Fetcher("https://www.fanfiction.net/s/555/2/My-Great-Story").ffnet_id == "555"
        assert ffnet.Fetcher("111").ffnet_id == "111"
        assert ffnet.Fetcher("a").ffnet_id is None
