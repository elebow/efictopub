from unittest.mock import MagicMock

from app.fetchers.ffnet import FFNet

from tests.fixtures.real import ffnet_chapter_html_real
from tests.fixtures.real import ffnet_chapter_2_html_real
import tests.fixtures.stubs


class TestFetchersFFNet:
    def test_fetch_story(self):
        tests.fixtures.stubs.return_values = [
            MagicMock(status_code=200, text=ffnet_chapter_html_real()),
            MagicMock(status_code=200, text=ffnet_chapter_2_html_real()),
            MagicMock(status_code=200, text="FanFiction.Net Message Type 1<hr size=1 noshade>Chapter not found.")
        ]
        fetcher = FFNet("https://www.fanfiction.net/s/555/8/")
        story = fetcher.fetch_story()
        assert story.title == "My Great Story"
        assert story.chapters[0].title == "1. Yes, these option tags are"
        assert [ch.text for ch in story.chapters] == [
            "Story Text *Goes* **Here**. Chapter 1.",
            "Story Text *Goes* **Here**. Chapter 2."
        ]

    def test_generate_chapter_htmls(self):
        tests.fixtures.stubs.return_values = [
            MagicMock(status_code=200, text="5"),
            MagicMock(status_code=200, text="6"),
            MagicMock(status_code=200, text="7"),
            MagicMock(status_code=200, text="FanFiction.Net Message Type 1<hr size=1 noshade>Chapter not found.")
        ]
        fetcher = FFNet("https://www.fanfiction.net/s/555/8/")
        htmls = [x for x in fetcher.generate_chapter_htmls()]
        assert htmls == ["5", "6", "7"]
