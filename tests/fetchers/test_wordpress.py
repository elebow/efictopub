from unittest.mock import MagicMock

from efictopub.fetchers import wordpress

from tests.fixtures.real import wordpress_chapter_html_real
import tests.fixtures.stubs


class TestFetchersWordpress:
    def test_fetch_blog_entries(self):
        tests.fixtures.stubs.return_values = [
            MagicMock(status_code=200, text=wordpress_chapter_html_real(1)),
            MagicMock(status_code=200, text=wordpress_chapter_html_real(2)),
        ]
        fetcher = wordpress.Fetcher("https://example.wordpress.com/")
        entries = fetcher.fetch_blog_entries()

        assert entries[0].entry_title == "Chapter 1.1"
        assert [entry.text for entry in entries] == [
            '<p dir="ltr">Chapter 1 content here\n</p>',
            '<p dir="ltr">Chapter 2 content here\n</p>',
        ]

    def test_fetch_story(self):
        tests.fixtures.stubs.return_values = [
            MagicMock(status_code=200, text=wordpress_chapter_html_real(1)),
            MagicMock(status_code=200, text=wordpress_chapter_html_real(2)),
        ]
        fetcher = wordpress.Fetcher("https://example.wordpress.com/")
        story = fetcher.fetch_story()

        assert (
            story.chapters[0].permalink
            == "https://blog-name.wordpress.com/2011/06/11/1-1/"
        )
