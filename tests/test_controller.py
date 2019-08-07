import argparse

from doubles import allow
from unittest.mock import call
from unittest.mock import MagicMock
from unittest.mock import patch

from app import git
from app.controller import Controller

from tests.fixtures.doubles import chapters_double, story_double


class TestController:
    def setup_method(self, method):
        self.parser = argparse.ArgumentParser()
        self.parser.add_argument("target")
        self.parser.add_argument("--fetcher", action="store")
        self.parser.add_argument("-o", action="store", dest="outfile")
        self.parser.add_argument(
            "--no-write-archive",
            action="store_false",
            dest="write_archive",
            default=True,
        )
        self.parser.add_argument(
            "--no-write-epub", action="store_false", dest="write_epub", default=True
        )

    @patch("reddit_next.Fetcher.fetch_chapters", lambda _x: chapters_double(3))
    @patch("app.archive.store")
    def test_fetch_from_reddit_next(self, archive):
        args = self.parser.parse_args(
            ["--fetcher", "reddit_next", "_whatever-url-or-id"]
        )
        subject = Controller(args)

        assert [chap.text for chap in subject.story.chapters] == [
            "<p>chapter content 0</p>",
            "<p>chapter content 1</p>",
            "<p>chapter content 2</p>",
        ]
        assert subject.story.author_name == "great author 0"

    @patch("reddit_author.Fetcher.fetch_chapters", lambda _x: chapters_double(3))
    @patch("app.archive.store")
    def test_fetch_from_reddit_author_by_url(self, archive):
        args = self.parser.parse_args(["reddit.com/u/some_redditor"])
        subject = Controller(args)

        assert [chap.text for chap in subject.story.chapters] == [
            "<p>chapter content 0</p>",
            "<p>chapter content 1</p>",
            "<p>chapter content 2</p>",
        ]
        assert subject.story.author_name == "great author 0"

    @patch("app.controller.Controller.archive_story")
    @patch("app.controller.Controller.output_story")
    def test_run(self, output_story, archive_story):
        args = self.parser.parse_args(["reddit.com/u/some_redditor"])
        subject = Controller(args)
        story = story_double()
        allow(subject).story.and_return(story)
        allow(git).repo_is_dirty.and_return(False)

        subject.run()

        output_story.assert_called_once()
        archive_story.assert_called_once()

    @patch("app.controller.Controller.archive_story")
    @patch("app.controller.Controller.output_story")
    def test_run_do_not_archive_when_fetcher_is_archive(
        self, output_story, archive_story
    ):
        args = self.parser.parse_args(
            ["--fetcher", "archive", "reddit.com/u/some_redditor"]
        )
        subject = Controller(args)
        story = story_double()
        allow(subject).story.and_return(story)
        allow(git).repo_is_dirty.and_return(False)

        subject.run()

        output_story.assert_called_once()
        archive_story.assert_not_called()

    @patch("app.controller.Controller.archive_story")
    @patch("app.controller.Controller.output_story")
    def test_run_do_not_archive_when_arg_not_present(self, output_story, archive_story):
        args = self.parser.parse_args(
            ["--no-write-archive", "reddit.com/u/some_redditor"]
        )
        subject = Controller(args)
        story = story_double()
        allow(subject).story.and_return(story)
        allow(git).repo_is_dirty.and_return(False)

        subject.run()

        output_story.assert_called_once()
        archive_story.assert_not_called()

    @patch("app.git.previous_commit_is_not_efic")
    @patch("app.git.commit_story")
    @patch("app.archive.store")
    def test_archive_and_git(
        self, archive_story, git_commit_story, previous_commit_is_not_efic
    ):
        args = self.parser.parse_args(["reddit.com/u/some_redditor"])
        subject = Controller(args)
        story = story_double()
        allow(subject).story.and_return(story)

        subject.archive_story()

        git_commit_story.assert_has_calls(
            [
                call(story, "Local changes before fetching great title"),
                call(story, "Fetch great title"),
            ]
        )
        archive_story.assert_called_once_with(story)

        previous_commit_is_not_efic.assert_called_once()

    @patch("app.controller.EpubWriter")
    def test_output_story_outfile(self, epub_writer):
        args = self.parser.parse_args(
            ["--fetcher", "archive", "-o", "great-outfile.epub", "whatever-target"]
        )
        subject = Controller(args)
        story = story_double()
        allow(subject).story.and_return(story)

        subject.output_story()

        epub_writer.assert_called_once_with(story, "great-outfile.epub")

    @patch("app.controller.EpubWriter")
    def test_output_story_no_outfile(self, epub_writer):
        args = self.parser.parse_args(["--fetcher", "archive", "whatever-id"])
        subject = Controller(args)
        story = story_double()
        allow(subject).story.and_return(story)

        subject.output_story()

        expected_path = f"$HOME/books/fic/{story.id}"
        epub_writer.assert_called_once_with(story, expected_path)
