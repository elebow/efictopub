import pytest
from unittest import mock
from unittest.mock import MagicMock
from unittest.mock import patch

from app.epub_writer import EpubWriter


@pytest.fixture
def story():
    return MagicMock(title="great-title",
                     author_name="great-author",
                     date_start="start-date",
                     date_end="end-date",
                     chapters=chapters())


@pytest.fixture
def chapters():
    return [MagicMock(title="chapter title 1", get_text=lambda: "content 1"),
            MagicMock(title="chapter title 2", get_text=lambda: "content 2")]


class TestEpubWriter:

    @patch("app.epub_writer.EpubWriter.add_chapters")
    @patch("ebooklib.epub.write_epub")
    def test_write_epub(self, write_epub_mock, add_chapters_mock, story):
        subject = EpubWriter(story, "outfile.epub")
        subject.write_epub()

        assert subject.book.title == "great-title"
        assert subject.book.language == "en"
        assert subject.book.metadata["http://purl.org/dc/elements/1.1/"]["creator"][0][0] == "great-author"
        write_epub_mock.assert_called_once_with("outfile.epub", mock.ANY)

    def test_add_chapters(self, story, chapters):
        subject = EpubWriter(story, "_outfile.epub")
        subject.add_chapters()

        assert [chap.file_name for chap in subject.book.items] == ["chap_0.xhtml", "chap_1.xhtml"]
        assert [chap.title for chap in subject.book.items] == ["chapter title 1", "chapter title 2"]
        assert [chap.content for chap in subject.book.items] == ["content 1", "content 2"]
