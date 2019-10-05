from doubles import allow
from unittest.mock import call
from unittest.mock import MagicMock
from unittest.mock import patch

from efictopub import config
from efictopub import git
from efictopub.models.reddit import RedditSubmission
from efictopub.efictopub import Efictopub

from tests.fixtures.doubles import praw_submissions_double, story_double


class TestEfictopub:
    def setup_method(self):
        config.config["fetcher_opts"] = ["title='Great Story'"]

    @patch("efictopub.efictopub.Efictopub.archive_story")
    @patch("efictopub.efictopub.Efictopub.output_story")
    def test_run(self, output_story, archive_story):
        args = {"target": "reddit.com/u/some_redditor"}
        subject = Efictopub(args)
        story = story_double()
        allow(subject.fetcher).fetch_story.and_return(story)
        allow(git).repo_is_dirty.and_return(False)

        subject.run()

        output_story.assert_called_once()
        archive_story.assert_called_once()

    @patch("efictopub.efictopub.Efictopub.archive_story")
    @patch("efictopub.efictopub.Efictopub.output_story")
    def test_run_do_not_archive_when_fetcher_is_archive(
        self, output_story, archive_story
    ):
        args = {"fetcher": "archive", "target": "reddit.com/u/some_redditor"}
        subject = Efictopub(args)
        subject.fetcher.__module__ = "archive"
        subject.fetcher.fetch_story = lambda: "aaa"
        allow(git).repo_is_dirty.and_return(False)

        subject.run()

        output_story.assert_called_once()
        archive_story.assert_not_called()

    @patch("efictopub.efictopub.Efictopub.archive_story")
    @patch("efictopub.efictopub.Efictopub.output_story")
    def test_run_do_not_archive_when_arg_not_present(self, output_story, archive_story):
        args = {"write_archive": False, "target": "reddit.com/u/some_redditor"}
        subject = Efictopub(args)
        story = story_double()
        allow(subject.fetcher).fetch_story.and_return(story)
        allow(git).repo_is_dirty.and_return(False)

        subject.run()

        output_story.assert_called_once()
        archive_story.assert_not_called()

    @patch("efictopub.git.previous_commit_is_not_efic")
    @patch("efictopub.git.commit_story")
    @patch("efictopub.archive.store")
    def test_archive_and_git(
        self, archive_store, git_commit_story, previous_commit_is_not_efic
    ):
        args = {"target": "reddit.com/u/some_redditor"}
        subject = Efictopub(args)
        story = story_double()
        allow(subject.fetcher).fetch_story.and_return(story)

        subject.archive_story(story)

        archive_store.assert_called_once_with(story)

        previous_commit_is_not_efic.assert_called_once()
