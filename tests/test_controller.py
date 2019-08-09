from doubles import allow
from unittest.mock import call
from unittest.mock import patch

from app import git
from app.models.reddit import RedditSubmission
from app.controller import Controller

from tests.fixtures.doubles import praw_submissions_double, story_double


class TestController:
    @patch(
        "reddit_next.Fetcher.fetch_submissions",
        lambda _x: [
            RedditSubmission(praw_sub) for praw_sub in praw_submissions_double(3)
        ],
    )
    @patch("app.archive.store")
    def test_fetch_from_reddit_next(self, archive):
        args = {"fetcher": "reddit_next", "target": "_whatever-url-or-id"}
        subject = Controller(args)

        assert [chap.text for chap in subject.story.chapters] == [
            "<p>some selftext_html</p>\n<p>second line</p>\n",
            "<p>some selftext_html</p>\n<p>second line</p>\n",
            "<p>some selftext_html</p>\n<p>second line</p>\n",
        ]
        assert subject.story.author == "redditor 0"

    @patch(
        "reddit_author.Fetcher.fetch_submissions",
        lambda _x: [
            RedditSubmission(praw_sub) for praw_sub in praw_submissions_double(3)
        ],
    )
    @patch("app.archive.store")
    def test_fetch_from_reddit_author_by_url(self, archive):
        args = {"target": "reddit.com/u/some_redditor"}
        subject = Controller(args)

        assert [chap.text for chap in subject.story.chapters] == [
            "<p>some selftext_html</p>\n<p>second line</p>\n",
            "<p>some selftext_html</p>\n<p>second line</p>\n",
            "<p>some selftext_html</p>\n<p>second line</p>\n",
        ]
        assert subject.story.author == "redditor 0"

    @patch("app.controller.Controller.archive_story")
    @patch("app.controller.Controller.output_story")
    def test_run(self, output_story, archive_story):
        args = {"target": "reddit.com/u/some_redditor"}
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
        args = {"fetcher": "archive", "target": "reddit.com/u/some_redditor"}
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
        args = {"write_archive": False, "target": "reddit.com/u/some_redditor"}
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
        args = {"target": "reddit.com/u/some_redditor"}
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
