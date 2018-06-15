from unittest import mock
from unittest.mock import patch

from app.epub_writer import EpubWriter

from tests.fixtures.doubles import story_double


class TestEpubWriter:

    @patch("app.epub_writer.EpubWriter.add_chapters")
    @patch("ebooklib.epub.write_epub")
    def test_write_epub(self, write_epub_mock, add_chapters_mock):
        subject = EpubWriter(story_double(), "outfile.epub")
        subject.write_epub()

        assert subject.book.title == "great title"
        assert subject.book.language == "en"
        assert subject.book.metadata["http://purl.org/dc/elements/1.1/"]["creator"][0][0] == "great author"
        write_epub_mock.assert_called_once_with("outfile.epub", mock.ANY)

    def test_add_chapters(self):
        subject = EpubWriter(story_double(), "_outfile.epub")
        subject.add_chapters()

        assert [chap.file_name for chap in subject.book.items] == \
            ["chap_0.xhtml", "chap_1.xhtml", "chap_2.xhtml"]
        assert [chap.title for chap in subject.book.items] == \
            ["chapter title 0", "chapter title 1", "chapter title 2"]
        assert [chap.content for chap in subject.book.items] == \
            ["chapter content 0", "chapter content 1", "chapter content 2"]
