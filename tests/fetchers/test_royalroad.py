import pytest

from efictopub import config
from efictopub.fetchers import royalroad

from tests.fixtures import royalroad_index_page_html
from tests.fixtures import royalroad_chapter_html_1
from tests.fixtures import royalroad_chapter_html_2


class TestFetchersRoyalroad:
    @pytest.fixture
    def mock_responses(self, requests_mock):
        requests_mock.get(
            "https://www.royalroad.com/fiction/555", text=royalroad_index_page_html
        )
        requests_mock.get(
            "https://www.royalroad.com/fiction/555/great-story/chapter/771/chapter-one",
            text=royalroad_chapter_html_1,
        )
        requests_mock.get(
            "https://www.royalroad.com/fiction/555/great-story/chapter/772/chapter-two",
            text=royalroad_chapter_html_2,
        )

    def test_fetch_story(self, mock_responses):
        story = royalroad.Fetcher("555").fetch_story()

        assert story.title == "Great Story"
        assert story.author == "Great Author"
        assert story.summary == "<p>Description here, untruncated</p>"
        assert story.date_start == 123
        assert story.date_end == 124
        assert len(story.chapters) == 2

    def test_fetch_chapters(self, mock_responses):
        chapters = royalroad.Fetcher("555").fetch_chapters()

        assert chapters[0].title == "Chapter One"
        assert chapters[1].title == "Chapter Two"

        assert chapters[0].author_name == "Great Author"
        assert chapters[0].comments == []
        assert (
            chapters[0].permalink
            == "https://www.royalroad.com/fiction/555/great-story/chapter/771/chapter-one"
        )
        assert chapters[0].score == 4.6
        assert chapters[0].summary is None
        assert chapters[0].text == (
            '<div class="portlet-title">\n'
            + '<div class="caption">\n'
            + '<i class="fa fa-sticky-note"></i>\n'
            + '<span class="caption-subject bold uppercase">A note from Great Author</span>\n'
            + "</div>\n"
            + "</div>\n"
            + '<div class="portlet-body author-note"><p>Author note bottom</p></div><p>Chapter One content</p><p>Author note bottom</p>'
        )

    def test_fetch_story_index(self, requests_mock):
        requests_mock.get(
            "https://www.royalroad.com/fiction/555", text=royalroad_index_page_html
        )
        story_index = royalroad.Fetcher("555").story_index

        assert story_index.chapter_urls == [
            "https://www.royalroad.com/fiction/555/great-story/chapter/771/chapter-one",
            "https://www.royalroad.com/fiction/555/great-story/chapter/772/chapter-two",
        ]
        assert story_index.title == "Great Story"
        assert story_index.author == "Great Author"
        assert story_index.summary == "<p>Description here, untruncated</p>"

    def test_calculate_rr_id(self):
        assert royalroad.Fetcher("555").rr_id == "555"
        assert (
            royalroad.Fetcher(
                "https://www.royalroad.com/fiction/555/great-story/chapter/772/chapter-one"
            ).rr_id
            == "555"
        )
        assert royalroad.Fetcher("www.royalroad.com/fiction/555").rr_id == "555"
        assert royalroad.Fetcher("http://royalroad.com/fiction/555").rr_id == "555"
        assert royalroad.Fetcher("abc").rr_id is None
