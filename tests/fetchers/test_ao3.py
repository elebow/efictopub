import pytest

from efictopub import config
from efictopub.fetchers import ao3
from efictopub.models.ao3.ao3_navigation_page import ChapterData

from tests.fixtures import ao3_navigation_page_html
from tests.fixtures import ao3_chapter_html_1
from tests.fixtures import ao3_chapter_html_2


class TestFetchersAO3:
    @pytest.fixture
    def mock_chapters_info(self, mocker):
        mocker.patch(
            "efictopub.fetchers.ao3.Fetcher.fetch_chapters_info",
            lambda self: [
                ChapterData(
                    url="https://www.archiveofourown.org/works/555/chapters/222",
                    date="2011-01-01",
                ),
                ChapterData(
                    url="https://www.archiveofourown.org/works/555/chapters/223",
                    date="2011-01-02",
                ),
            ],
        )

    @pytest.fixture
    def mock_chapters(self, requests_mock):
        requests_mock.get(
            "https://www.archiveofourown.org/works/555/chapters/222",
            text=ao3_chapter_html_1,
        )
        requests_mock.get(
            "https://www.archiveofourown.org/works/555/chapters/223",
            text=ao3_chapter_html_2,
        )

    def test_fetch_story(self, mock_chapters_info, mock_chapters):
        story = ao3.Fetcher("https://www.archiveofourown.org/works/555").fetch_story()

        assert story.title == "My Great Story"
        assert story.author == "user1"
        assert story.summary == "story summary"
        assert story.date_start == 1293858000
        assert len(story.chapters) == 2

    def test_fetch_chapters(self, mock_chapters_info, mock_chapters):
        chapters = ao3.Fetcher(
            "https://www.archiveofourown.org/works/555"
        ).fetch_chapters()

        assert chapters[0].title == "Prologue"
        assert chapters[1].title == "Chapter 2"

    def test_fetch_chapters_info(self, requests_mock):
        requests_mock.get(
            "https://www.archiveofourown.org/works/555/navigate",
            text=ao3_navigation_page_html,
        )
        chapters_info = ao3.Fetcher(
            "https://www.archiveofourown.org/works/555"
        ).fetch_chapters_info()
        assert len(chapters_info) == 3
        assert [chapter.url for chapter in chapters_info] == [
            "https://www.archiveofourown.org/works/555/chapters/880",
            "https://www.archiveofourown.org/works/555/chapters/881",
            "https://www.archiveofourown.org/works/555/chapters/882",
        ]

    def test_calculate_ao3_id(self):
        assert ao3.Fetcher("555").ao3_id == "555"
        assert (
            ao3.Fetcher(
                "https://www.archiveofourown.org/works/555/chapters/222#workskin"
            ).ao3_id
            == "555"
        )
        assert ao3.Fetcher("www.archiveofourown.org/works/555").ao3_id == "555"
        assert ao3.Fetcher("http://archiveofourown.org/works/555").ao3_id == "555"
        assert ao3.Fetcher("abc").ao3_id is None
