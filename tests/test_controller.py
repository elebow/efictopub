from doubles import allow
from unittest.mock import call
from unittest.mock import MagicMock
from unittest.mock import patch


from app.controller import Controller

from tests.fixtures.doubles import chapters_double, story_double


class TestController:

    @patch("app.fetchers.RedditNext.fetch_chapters", lambda _x: chapters_double(3))
    @patch("app.archive.store")
    def test_fetch_from_reddit_next(self, archive):
        args = MagicMock(fetcher="reddit_next", target="_whatever-url-or-id")
        subject = Controller(args)
        story = subject.get_story()

        assert [chap.text for chap in story.chapters] == \
            ["chapter content 0", "chapter content 1", "chapter content 2"]
        assert story.author_name == "great author 0"

    @patch("app.fetchers.RedditAuthor.fetch_chapters", lambda _x: chapters_double(3))
    @patch("app.archive.store")
    def test_fetch_from_reddit_author_by_url(self, archive):
        args = MagicMock(fetcher=None, target="reddit.com/u/some_redditor")
        subject = Controller(args)
        story = subject.get_story()

        assert [chap.text for chap in story.chapters] == \
            ["chapter content 0", "chapter content 1", "chapter content 2"]
        assert story.author_name == "great author 0"

    @patch("app.config.archive", MagicMock(location="/path/to/archive"))
    @patch("app.git.commit_story")
    @patch("app.archive.store")
    def test_archive_and_git(self, archive_story, git_commit_story):
        args = MagicMock(fetcher=None, target="reddit.com/u/some_redditor")
        subject = Controller(args)
        story = story_double()
        allow(subject).story.and_return(story)

        subject.archive_story()

        git_commit_story.assert_has_calls([
            call(story, "Local changes before fetching great title"),
            call(story, "Fetch great title")
        ])
        archive_story.assert_called_once_with(story)
