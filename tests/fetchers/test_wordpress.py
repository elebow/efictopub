from unittest.mock import MagicMock

from efictopub import config
from efictopub.fetchers import wordpress

from tests.fixtures.real import wordpress_chapter_html_real
import tests.fixtures.stubs


class TestFetchersWordpress:
    def setup_method(self):
        config.config["fetcher_opts"] = ["title='Great Story'", "author='Great Author'"]

    def test_fetch_blog_entries(self):
        tests.fixtures.stubs.return_values = [
            MagicMock(status_code=200, text=wordpress_chapter_html_real(1)),
            MagicMock(status_code=200, text=wordpress_chapter_html_real(2)),
        ]
        fetcher = wordpress.Fetcher("https://blog-name.wordpress.com/2011/06/11/1-1/")
        entries = fetcher.fetch_blog_entries()

        assert len(entries) == 2
        assert entries[0].entry_title == "Chapter 1.1"
        assert [entry.text for entry in entries] == [
            '<p dir="ltr">Chapter 1 content here\n</p>',
            '<p dir="ltr">Chapter 2 <b>content</b> here\n</p>',
        ]
        assert [entry.date_published for entry in entries] == [1307768479, 1307768479]
        assert [entry.date_updated for entry in entries] == [1412115014, None]

    def test_fetch_story(self):
        tests.fixtures.stubs.return_values = [
            MagicMock(status_code=200, text=wordpress_chapter_html_real(1)),
            MagicMock(status_code=200, text=wordpress_chapter_html_real(2)),
        ]
        fetcher = wordpress.Fetcher("https://blog-name.wordpress.com/2011/06/11/1-1/")
        story = fetcher.fetch_story()

        assert (
            story.chapters[0].permalink
            == "https://blog-name.wordpress.com/2011/06/11/1-1/"
        )
        assert story.author == "author-name"

    def test_last_chapter_pattern(self):
        config.config["fetcher_opts"] = [
            "title='Great Story'",
            "author='Great Author'",
            "last_chapter_pattern=2011/06/11",
        ]
        tests.fixtures.stubs.return_values = [
            MagicMock(status_code=200, text=wordpress_chapter_html_real(1)),
            MagicMock(status_code=200, text=wordpress_chapter_html_real(2)),
        ]
        fetcher = wordpress.Fetcher("https://blog-name.wordpress.com/2011/06/11/1-1/")
        entries = fetcher.fetch_blog_entries()

        assert len(entries) == 1
        assert entries[0].entry_title == "Chapter 1.1"
        assert [entry.text for entry in entries] == [
            '<p dir="ltr">Chapter 1 content here\n</p>'
        ]

    def test_comments(self):
        config.config["fetcher_opts"] = [
            "title='Great Story'",
            "author='Great Author'",
            "last_chapter_pattern=2011/06/11",
        ]
        tests.fixtures.stubs.return_values = [
            MagicMock(status_code=200, text=wordpress_chapter_html_real(1))
        ]
        fetcher = wordpress.Fetcher("https://blog-name.wordpress.com/2011/06/11/1-1/")
        entry = fetcher.fetch_blog_entries()[0]

        assert entry.comments[0].author == "commenter 1"
        assert entry.comments[0].text == "<p>comment 1 text</p>"

        assert entry.comments[0].replies[0].author == "commenter 2"
        assert entry.comments[0].replies[0].text == "<p>comment 2 text</p>"

        assert entry.comments[0].replies[0].replies[0].author == "commenter 3"
        assert entry.comments[0].replies[0].replies[0].text == "<p>comment 3 text</p>"

        assert entry.comments[1].author == "commenter 4"
        assert entry.comments[1].text == "<p>comment 4 text</p>"
