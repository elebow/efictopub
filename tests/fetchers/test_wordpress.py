from efictopub import config
from efictopub.fetchers import wordpress

import pytest

from tests.fixtures import wordpress_chapter_html_real_1
from tests.fixtures import wordpress_chapter_html_real_2


class TestFetchersWordpress:
    @pytest.fixture(autouse=True)
    def base_config(self):
        config.config["fetcher_opts"] = ["title='Great Story'", "author='Great Author'"]

    def test_fetch_blog_entries(self, requests_mock):
        requests_mock.get(
            "https://blog-name.wordpress.com/2011/06/11/1-1/",
            text=wordpress_chapter_html_real_1,
        )
        requests_mock.get(
            "https://blog-name.wordpress.com/2011/06/14/chapter-1-2/",
            text=wordpress_chapter_html_real_2,
        )

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

    def test_fetch_story(self, requests_mock):
        requests_mock.get(
            "https://blog-name.wordpress.com/2011/06/11/1-1/",
            text=wordpress_chapter_html_real_1,
        )
        requests_mock.get(
            "https://blog-name.wordpress.com/2011/06/14/chapter-1-2/",
            text=wordpress_chapter_html_real_2,
        )

        fetcher = wordpress.Fetcher("https://blog-name.wordpress.com/2011/06/11/1-1/")
        story = fetcher.fetch_story()

        assert (
            story.chapters[0].permalink
            == "https://blog-name.wordpress.com/2011/06/11/1-1/"
        )
        assert story.author == "author-name"

    def test_last_chapter_pattern(self, requests_mock):
        config.config["fetcher_opts"] = [
            "title='Great Story'",
            "author='Great Author'",
            "last_chapter_pattern=2011/06/11",
        ]
        requests_mock.get(
            "https://blog-name.wordpress.com/2011/06/11/1-1/",
            text=wordpress_chapter_html_real_1,
        )

        fetcher = wordpress.Fetcher("https://blog-name.wordpress.com/2011/06/11/1-1/")
        entries = fetcher.fetch_blog_entries()

        assert len(entries) == 1
        assert entries[0].entry_title == "Chapter 1.1"
        assert [entry.text for entry in entries] == [
            '<p dir="ltr">Chapter 1 content here\n</p>'
        ]

    def test_comments(self, requests_mock):
        config.config["fetcher_opts"] = [
            "title='Great Story'",
            "author='Great Author'",
            "last_chapter_pattern=2011/06/11",
        ]
        requests_mock.get(
            "https://blog-name.wordpress.com/2011/06/11/1-1/",
            text=wordpress_chapter_html_real_1,
        )

        fetcher = wordpress.Fetcher("https://blog-name.wordpress.com/2011/06/11/1-1/")
        entry = fetcher.fetch_blog_entries()[0]

        assert len(entry.comments) == 3
        assert entry.comments[0].author == "commenter 1"
        assert entry.comments[0].text == "<p>comment 1 text</p>"

        assert len(entry.comments[0].replies) == 1
        assert entry.comments[0].replies[0].author == "commenter 2"
        assert entry.comments[0].replies[0].text == "<p>comment 2 text</p>"

        assert len(entry.comments[0].replies[0].replies) == 1
        assert entry.comments[0].replies[0].replies[0].author == "commenter 3"
        assert entry.comments[0].replies[0].replies[0].text == "<p>comment 3 text</p>"

        assert len(entry.comments[1].replies) == 0
        assert entry.comments[1].author == "commenter 4"
        assert entry.comments[1].text == "<p>comment 4 text</p>"

        assert len(entry.comments[2].replies) == 2
        assert len(entry.comments[2].replies[0].replies) == 1

    def test_comments_only_author(self, requests_mock):
        config.config["fetcher_opts"] = [
            "title='Great Story'",
            "author='Great Author'",
            "last_chapter_pattern=2011/06/11",
            "author_only_replies=commenter 2",
        ]
        requests_mock.get(
            "https://blog-name.wordpress.com/2011/06/11/1-1/",
            text=wordpress_chapter_html_real_1,
        )

        fetcher = wordpress.Fetcher("https://blog-name.wordpress.com/2011/06/11/1-1/")
        entry = fetcher.fetch_blog_entries()[0].as_chapter()

        assert len(entry.comments) == 1
        assert entry.comments[0].author == "commenter 1"
        assert entry.comments[0].text == "<p>comment 1 text</p>"

        assert entry.comments[0].replies[0].author == "commenter 2"
        assert entry.comments[0].replies[0].text == "<p>comment 2 text</p>"

        assert len(entry.comments[0].replies[0].replies) == 0
