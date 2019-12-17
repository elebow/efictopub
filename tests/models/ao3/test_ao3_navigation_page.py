from efictopub.models.ao3.ao3_navigation_page import AO3NavigationPage

import pytest

from tests.fixtures import ao3_navigation_page_html


class TestAO3NavigationPage:
    @pytest.fixture
    def ao3_navigation_page(self):
        return AO3NavigationPage(ao3_navigation_page_html)

    def test_chapters(self, ao3_navigation_page):
        chapters = ao3_navigation_page.chapters

        assert (
            chapters[0].url == "https://www.archiveofourown.org/works/555/chapters/880"
        )
        assert chapters[0].date == "2015-06-16"
        assert (
            chapters[1].url == "https://www.archiveofourown.org/works/555/chapters/881"
        )
        assert chapters[1].date == "2015-06-17"
        assert (
            chapters[2].url == "https://www.archiveofourown.org/works/555/chapters/882"
        )
        assert chapters[2].date == "2015-06-18"
