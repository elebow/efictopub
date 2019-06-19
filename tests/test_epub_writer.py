from datetime import datetime
from ebooklib import epub

from doubles import allow
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
        assert (
            subject.book.metadata["http://purl.org/dc/elements/1.1/"]["creator"][0][0]
            == "great author"
        )
        write_epub_mock.assert_called_once_with(
            "outfile.epub", mock.ANY, {"mtime": datetime(2015, 7, 27, 12, 26, 40)}
        )

    def test_add_info_page(self):
        allow(epub).write_epub

        subject = EpubWriter(story_double(), "outfile.epub")
        subject.write_epub()

        assert subject.book.items[2].content == "great title<br>by great author"

    def test_add_chapters(self):
        subject = EpubWriter(story_double(), "_outfile.epub")
        subject.add_chapters()

        assert [chap.file_name for chap in subject.book.items] == [
            "chap_000.xhtml",
            "chap_001.xhtml",
            "chap_002.xhtml",
        ]
        assert [chap.title for chap in subject.book.items] == [
            "chapter title 0",
            "chapter title 1",
            "chapter title 2",
        ]
        assert [chap.content for chap in subject.book.items] == [
            "chapter title 0\n\n<p>chapter content 0</p>",
            "chapter title 1\n\n<p>chapter content 1</p>",
            "chapter title 2\n\n<p>chapter content 2</p>",
        ]

    def test_add_toc(self):
        subject = EpubWriter(story_double(), "_outfile.epub")
        subject.add_toc()

        assert isinstance(subject.book.toc, tuple)
        assert [item.__class__ for item in subject.book.toc] == [epub.EpubHtml] * 3
        assert [item.file_name for item in subject.book.toc] == [
            "chap_000.xhtml",
            "chap_001.xhtml",
            "chap_002.xhtml",
        ]
