from efictopub.models.ao3.ao3_chapter import AO3Chapter

import pytest

from tests.fixtures import ao3_chapter_html_1


class TestAO3Chapter:
    @pytest.fixture
    def ao3_chapter(self):
        return AO3Chapter(ao3_chapter_html_1, "date_published")

    def test_as_chapter(self, ao3_chapter):
        chapter = ao3_chapter.as_chapter()

        assert chapter.comments == []
        assert chapter.date_published == "date_published"
        assert chapter.date_updated is None
        assert chapter.permalink == "https://www.archiveofourown.org/chapters/880"
        assert chapter.score == 14369
        assert chapter.text == "Chapter 1 text."
        assert chapter.title == "Prologue"
