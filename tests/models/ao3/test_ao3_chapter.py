from efictopub.models.ao3.ao3_chapter import AO3Chapter

import pytest

from tests.fixtures import ao3_chapter_html_1
from tests.fixtures import ao3_single_chapter_story_html


class TestAO3Chapter:
    def test_as_chapter(self):
        chapter = AO3Chapter(
            ao3_chapter_html_1,
            "todo comments html",  # TODO
            date_published="2017-08-09",
        ).as_chapter()

        assert chapter.comments == []
        assert chapter.date_published == 1502251200
        assert chapter.date_updated == 0
        assert chapter.permalink == "https://www.archiveofourown.org/chapters/880"
        assert chapter.score == 14369
        assert chapter.text == "<p>Chapter 1 text.</p>"
        assert chapter.title == "Prologue"

    def test_as_chapter_single_chapter_story(self):
        chapter = AO3Chapter(
            ao3_single_chapter_story_html,
            "todo comments html",  # TODO
            date_published="2017-08-09",
        ).as_chapter()

        assert chapter.comments == []
        assert chapter.date_published == 1502251200
        assert chapter.date_updated == 0
        assert chapter.permalink == "https://www.archiveofourown.org/chapters/235"
        assert chapter.score == 565
        assert chapter.text == "<p>story contents here</p>"
        assert chapter.title == "Single-Chapter Story"
