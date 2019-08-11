from datetime import datetime
from ebooklib import epub

from doubles import allow
from freezegun import freeze_time
from unittest import mock
from unittest.mock import patch

from app import config
from app.epub_writer import EpubWriter

from tests.fixtures.real import story_real


class TestEpubWriter:
    @patch("app.epub_writer.EpubWriter.add_chapters")
    @patch("ebooklib.epub.write_epub")
    def test_write_epub(self, write_epub_mock, add_chapters_mock):
        config.config["outfile"] = "outfile.epub"
        subject = EpubWriter(story_real())
        subject.write_epub()

        assert subject.book.title == "My Great Story"
        assert subject.book.language == "en"
        assert (
            subject.book.metadata["http://purl.org/dc/elements/1.1/"]["creator"][0][0]
            == "Great Author"
        )
        write_epub_mock.assert_called_once_with(
            "outfile.epub", mock.ANY, {"mtime": datetime(1970, 1, 1, 0, 0, 21)}
        )

    def test_add_info_page(self):
        allow(epub).write_epub

        subject = EpubWriter(story_real())
        subject.write_epub()

        assert subject.book.items[2].content == "My Great Story<br>by Great Author"

    def test_add_chapters(self):
        subject = EpubWriter(story_real())
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
        subject = EpubWriter(story_real())
        subject.add_toc()

        assert isinstance(subject.book.toc, tuple)
        assert [item.__class__ for item in subject.book.toc] == [epub.EpubHtml] * 3
        assert [item.file_name for item in subject.book.toc] == [
            "chap_000.xhtml",
            "chap_001.xhtml",
            "chap_002.xhtml",
        ]

    def test_output_filename_config(self):
        config.config["outfile"] = "great-outfile.epub"
        subject = EpubWriter(story_real())

        assert subject.output_filename() == "great-outfile.epub"

    def test_output_filename_auto(self):
        config.config["outfile"] = ""
        story = story_real()
        subject = EpubWriter(story)

        assert (
            subject.output_filename()
            == f"$HOME/books/fic/My Great Story - Great Author"
        )
