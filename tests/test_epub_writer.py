from efictopub import config
from efictopub.epub_writer import EpubWriter


class TestEpubWriter:
    def test_write_epub(self, mocker, story_factory, chapter_factory):
        mocker.patch("mkepub.Book.add_page")
        mocker.patch("mkepub.Book.set_cover")
        mocker.patch("mkepub.Book.save")
        config.config["outfile"] = "x.epub"
        writer = EpubWriter(
            story_factory.build(
                title="My Great Story",
                author="Great Author",
                chapters=[chapter_factory.build(date_published=0, date_updated=21)],
            )
        )

        writer.write_epub()

        assert writer.book.title == "My Great Story"
        assert writer.book.metadata == {
            "published": "1970-01-01T00:00:21",
            "author": "Great Author",
            "dcterms": {"available": "1970-01-01T00:00:00"},
        }

    def test_add_chapters(self, mocker, story_factory, chapter_factory):
        mocker.patch("mkepub.Book.add_page")
        chapter_factory.reset_sequence(0)
        writer = EpubWriter(story_factory.build(num_chapters=3))

        writer.add_chapters()

        writer.book.add_page.assert_has_calls(
            [
                mocker.call(
                    "Chapter Title 0",
                    "<h2 class='chapter-header'><em>Chapter Title 0</em></h2><p>chapter content 0</p>",
                ),
                mocker.call(
                    "Chapter Title 1",
                    "<h2 class='chapter-header'><em>Chapter Title 1</em></h2><p>chapter content 1</p>",
                ),
                mocker.call(
                    "Chapter Title 2",
                    "<h2 class='chapter-header'><em>Chapter Title 2</em></h2><p>chapter content 2</p>",
                ),
            ]
        )

    def test_add_chapters_with_comments(
        self, mocker, story_factory, chapter_factory, comment_factory
    ):
        config.config["fetch_comments"] = True
        mocker.patch("mkepub.Book.add_page")

        chapter_factory.reset_sequence(0)
        comment_factory.reset_sequence(0)
        comments = [comment_factory.build(tree_depth=2)]
        story = story_factory.build(num_chapters=1)
        story.chapters[0].comments = comments

        writer = EpubWriter(story)
        writer.add_chapters()

        writer.book.add_page.assert_has_calls(
            [
                mocker.call(
                    "Chapter Title 0",
                    "<p>chapter content 0</p>"
                    "<h3>Comments</h3>"
                    "<div class='comments'>"
                    "<div class='comment'>"
                    "<p>Comment Author Name 0 (1970-01-01, edited 1970-01-01)</p>"
                    "<p>text 0</p>"
                    "<div class='replies'>"
                    "<div class='comment'>"
                    "<p>Comment Author Name 1 (1970-01-01, edited 1970-01-01)</p>"
                    "<p>text 1</p>"
                    "</div>"
                    "</div>"
                    "</div>"
                    "</div>",
                )
            ]
        )

    def test_output_filename_config(self, story_factory):
        config.config["outfile"] = "great-outfile.epub"
        writer = EpubWriter(story_factory.build())

        assert writer.output_filename() == "great-outfile.epub"

    def test_output_filename_auto(self, story_factory):
        config.config["outfile"] = ""
        config.config["epub_location"] = "/some/epub/location"
        writer = EpubWriter(
            story_factory.build(title="My Great Story", author="Great Author")
        )

        assert (
            writer.output_filename()
            == f"/some/epub/location/My Great Story - Great Author.epub"
        )
