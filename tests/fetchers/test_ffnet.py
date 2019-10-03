from unittest.mock import MagicMock

from efictopub import config
from efictopub.fetchers import ffnet

from tests.fixtures.real import ffnet_chapter_html_real
from tests.fixtures.real import ffnet_chapter_2_html_real
from tests.fixtures.real import ffnet_chapter_3_html_real
from tests.fixtures.real import ffnet_single_chapter_story_html_real
from tests.fixtures.real import ffnet_single_chapter_story_reviews_html_real
from tests.fixtures.stubs import stub_response


class TestFetchersFFNet:
    def test_fetch_story(self):
        stub_response(ffnet_chapter_html_real())
        stub_response(
            "<div id='content_wrapper_inner'><td><div>ch 1 review</div></td></div>"
        )
        stub_response(ffnet_chapter_2_html_real())
        stub_response(
            "<div id='content_wrapper_inner'><td><div>ch 2 review</div></td></div>"
        )
        stub_response(ffnet_chapter_3_html_real())
        stub_response(
            "<div id='content_wrapper_inner'><td><div>ch 3 review</div></td></div>"
        )

        fetcher = ffnet.Fetcher("https://www.fanfiction.net/s/555/8/")
        story = fetcher.fetch_story()
        assert story.title == "My Great Story"
        assert story.chapters[0].title == "1. Yes, these option tags are"
        assert [ch.text for ch in story.chapters] == [
            "<p>\n    Story Text <em>Goes</em> <strong>Here</strong>. Chapter 1.\n    </p>",
            "<p>\n    Story Text <em>Goes</em> <strong>Here</strong>. Chapter 2.\n    </p>",
            "<p>\n    Story Text <em>Goes</em> <strong>Here</strong>. Chapter 3.\n    </p>",
        ]
        assert [
            comment[0].text for comment in [ch.comments for ch in story.chapters]
        ] == ["ch 1 review", "ch 2 review", "ch 3 review"]

    def test_generate_chapters_for_single_chapter_story(self):
        stub_response(ffnet_single_chapter_story_html_real())
        stub_response(ffnet_single_chapter_story_reviews_html_real())

        fetcher = ffnet.Fetcher("https://www.fanfiction.net/s/555/8/")
        htmls = [x for x in fetcher.generate_ffnet_chapters()]
        assert len(htmls) == 1
        assert (
            htmls[0].text
            == "<p>\n       Story Text <em>Goes</em> <strong>Here</strong>.\n       </p>"
        )

    def test_calculate_ffnet_id(self):
        assert ffnet.Fetcher("https://www.fanfiction.net/s/555/8/").ffnet_id == "555"
        assert (
            ffnet.Fetcher("https://www.fanfiction.net/s/555/2/My-Great-Story").ffnet_id
            == "555"
        )
        assert ffnet.Fetcher("111").ffnet_id == "111"
        assert ffnet.Fetcher("a").ffnet_id is None

    def test_fetch_comments(self):
        config.config["fetch_comments"] = True

        stub_response(ffnet_single_chapter_story_html_real())
        stub_response(ffnet_single_chapter_story_reviews_html_real())

        chapters = ffnet.Fetcher("https://www.fanfiction.net/s/555/8/").fetch_chapters()
        assert [len(chapter.reviews) for chapter in chapters] == [3]

    def test_skip_comments(self):
        config.config["fetch_comments"] = False

        stub_response(ffnet_single_chapter_story_html_real())

        chapters = ffnet.Fetcher("https://www.fanfiction.net/s/555/8/").fetch_chapters()
        assert [len(chapter.reviews) for chapter in chapters] == [0]
