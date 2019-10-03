from efictopub.models.ffnet.ffnet_chapter import FFNetChapter

from tests.fixtures.real import ffnet_chapter_html_real


class TestFFNetChapter:
    def setup_method(self):
        chapter_html = ffnet_chapter_html_real
        self.subject = FFNetChapter(chapter_html)

    def test_set_fields_from_html(self):
        assert self.subject.author_name == "Great Author"
        assert self.subject.chapter_title == "1. Yes, these option tags are"
        assert self.subject.score == "5,555"
        assert self.subject.date_updated == 1290054512
        assert self.subject.date_published == 1279499410
        assert (
            self.subject.permalink
            == "https://www.fanfiction.net/s/555/1/My-Great-Story"
        )
        assert (
            self.subject.text
            == "<p>\n    Story Text <em>Goes</em> <strong>Here</strong>. Chapter 1.\n    </p>"
        )
        assert self.subject.reviews == []

    def test_as_chapter(self):
        chapter = self.subject.as_chapter()

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
