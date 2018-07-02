from app.models.ffnet.ffnet_chapter import FFNetChapter

from tests.fixtures.real import ffnet_chapter_html_real


class TestFFnetChapter:
    def setup_method(self):
        html = ffnet_chapter_html_real()
        self.subject = FFNetChapter(html)

    def test_set_fields_from_html(self):
        assert self.subject.author_name == "Great Author"
        assert self.subject.title == "1. Yes, these option tags are"
        assert self.subject.score == "5,555"
        assert self.subject.date_updated == 1290054512
        assert self.subject.date_published == 1279499410
        assert self.subject.ffnet_id == "555"
        assert self.subject.permalink == "https://www.fanfiction.net/s/555/1/My-Great-Story"
        assert self.subject.text == "Story Text *Goes* **Here**. Chapter 1."
        assert self.subject.reviews == []

    def test_as_chapter(self):
        chapter = self.subject.as_chapter()

        assert chapter.author == "Great Author"
        assert chapter.comments == []
        assert chapter.date_published == 1279499410
        assert chapter.date_updated == 1290054512
        assert chapter.permalink == "https://www.fanfiction.net/s/555/1/My-Great-Story"
        assert chapter.score == "5,555"
        assert chapter.text == "Story Text *Goes* **Here**. Chapter 1."
        assert chapter.title == "1. Yes, these option tags are"
