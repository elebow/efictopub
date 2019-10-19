from efictopub.models.ffnet.ffnet_chapter import FFNetChapter

import pytest

from tests.fixtures import ffnet_chapter_html_real


class TestFFNetChapter:
    @pytest.fixture(autouse=True)
    def ffnet_chapter(self):
        return FFNetChapter(ffnet_chapter_html_real)

    def test_set_fields_from_html(self, ffnet_chapter):
        assert ffnet_chapter.author_name == "Great Author"
        assert ffnet_chapter.chapter_title == "1. Yes, these option tags are"
        assert ffnet_chapter.score == "5,555"
        assert ffnet_chapter.date_updated == 1290054512
        assert ffnet_chapter.date_published == 1279499410
        assert (
            ffnet_chapter.permalink
            == "https://www.fanfiction.net/s/555/1/My-Great-Story"
        )
        assert (
            ffnet_chapter.text
            == "<p>\n    Story Text <em>Goes</em> <strong>Here</strong>. Chapter 1.\n    </p>"
        )
        assert ffnet_chapter.reviews == []

    def test_as_chapter(self, ffnet_chapter):
        chapter = ffnet_chapter.as_chapter()

        assert chapter.comments == []
        assert chapter.date_published == 1279499410
        assert chapter.date_updated == 1290054512
        assert chapter.permalink == "https://www.fanfiction.net/s/555/1/My-Great-Story"
        assert chapter.score == "5,555"
        assert (
            chapter.text
            == "<p>\n    Story Text <em>Goes</em> <strong>Here</strong>. Chapter 1.\n    </p>"
        )
        assert chapter.title == "1. Yes, these option tags are"

    def test_is_last_chapter(self):
        assert (
            FFNetChapter(
                "<select id='chap_select'><option selected>1</option><option>2</option></select><div id='storytext'></div>"
            ).is_last_chapter()
            is False
        )

        assert (
            FFNetChapter(
                "<select id='chap_select'><option>1</option><option selected>2</option></select><div id='storytext'></div>"
            ).is_last_chapter()
            is True
        )
