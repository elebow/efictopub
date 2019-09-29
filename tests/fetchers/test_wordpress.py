from unittest.mock import MagicMock

from efictopub.fetchers import wordpress

from tests.fixtures.real import wordpress_chapter_html_real
import tests.fixtures.stubs


class TestFetchersWordpress:
    def test_fetch_blog_entries(self):
        tests.fixtures.stubs.return_values = [
            MagicMock(status_code=200, text=wordpress_chapter_html_real())
        ]
        fetcher = wordpress.Fetcher("https://example.wordpress.com/")
        entries = fetcher.fetch_blog_entries()

        assert entries[0].entry_title == "Chapter 1.1"
        assert [entry.text for entry in entries] == [
            '<p dir="ltr">Chapter 1 content here\n</p>'
        ]
