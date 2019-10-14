from efictopub import config
from efictopub.epub_writer import EpubWriter

from tests.fixtures.real import story_real


class TestEpubWriter:
    def test_write_epub(self, mocker):
        mocker.patch("mkepub.Book.add_page")
        mocker.patch("mkepub.Book.set_cover")
        mocker.patch("mkepub.Book.save")
        config.config["outfile"] = "x.epub"
        writer = EpubWriter(story_real())

        writer.write_epub()

        assert writer.book.title == "My Great Story"
        assert writer.book.metadata == {
            "published": "1970-01-01T00:00:21",
            "author": "Great Author",
            "dcterms": {"available": "1970-01-01T00:00:00"},
        }

    def test_add_chapters(self, mocker):
        mocker.patch("mkepub.Book.add_page")
        writer = EpubWriter(story_real())

        writer.add_chapters()

        assert writer.book.add_page.has_calls(
            [
                mocker.call("chapter title 0", "chapter content 0"),
                mocker.call("chapter title 1", "chapter content 1"),
                mocker.call("chapter title 2", "chapter content 2"),
            ]
        )

    def test_output_filename_config(self):
        config.config["outfile"] = "great-outfile.epub"
        subject = EpubWriter(story_real())

        assert subject.output_filename() == "great-outfile.epub"

    def test_output_filename_auto(self):
        config.config["outfile"] = ""
        config.config["epub_location"] = "/some/epub/location"
        subject = EpubWriter(story_real())

        assert (
            subject.output_filename()
            == f"/some/epub/location/My Great Story - Great Author.epub"
        )
