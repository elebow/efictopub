import pytest
from unittest.mock import MagicMock
from unittest.mock import patch
from unittest import mock

from app.lib import reddit_util
from app.models import reddit
from app import exceptions

from tests.fixtures.doubles import praw_submissions


subreddit_inst = MagicMock()
subreddit_class = MagicMock(return_value=subreddit_inst)


class TestRedditUtil:

    def setup_method(self):
        self.subject = reddit_util
        self.praw_reddit = MagicMock()

    @patch("app.lib.reddit_util.parse_url")
    def test_parse_id_or_url_submission(self, parse_url):
        submission_url = praw_submissions[0].permalink
        self.subject.parse_id_or_url(submission_url, self.praw_reddit)
        self.subject.parse_url.assert_called_once_with(submission_url, self.praw_reddit)

    @patch("app.lib.reddit_util.parse_url")
    def test_parse_id_or_url_comment(self, parse_url):
        comment_url = praw_submissions[0].comments[0].permalink
        self.subject.parse_id_or_url(comment_url, self.praw_reddit)
        self.subject.parse_url.assert_called_once_with(comment_url, self.praw_reddit)

    @patch("app.lib.reddit_util.parse_url")
    def test_parse_id_or_url_wikipage(self, parse_url):
        wikipage_url = "reddit.com/r/whatever/wiki/pagename"
        self.subject.parse_id_or_url(wikipage_url, self.praw_reddit)
        self.subject.parse_url.assert_called_once_with(wikipage_url, self.praw_reddit)

    @patch("app.lib.reddit_util.parse_url")
    def test_parse_id_or_url_ambiguous(self, parse_url):
        # ambiguous id
        with pytest.raises(exceptions.AmbiguousIdError):
            self.subject.parse_id_or_url('aaaaaa', self.praw_reddit)

    @patch("praw.models.Submission")
    @patch("praw.models.Comment")
    @patch("praw.models.WikiPage")
    @patch("praw.models.Subreddit", subreddit_class)
    def test_parse_url(self, wikipage_class, comment_class, submission_class):
        submission_url = 'https://reddit.com/r/my_great_subreddit/comments/a123/my_great_title/'
        comment_url = 'https://reddit.com/r/my_great_subreddit/comments/a123/my_great_title/b456/'
        wiki_url = 'https://reddit.com/r/my_great_subreddit/wiki/some/page/name'

        result = self.subject.parse_url(submission_url, self.praw_reddit)
        assert isinstance(result, reddit.Submission)
        submission_class.assert_called_once_with(self.praw_reddit, url=submission_url)

        result = self.subject.parse_url(comment_url, self.praw_reddit)
        assert isinstance(result, reddit.Comment)
        comment_class.assert_called_once_with(self.praw_reddit, url=comment_url)

        result = self.subject.parse_url(wiki_url, self.praw_reddit)
        assert isinstance(result, reddit.WikiPage)
        subreddit_class.assert_called_once_with(self.praw_reddit, "my_great_subreddit")
        wikipage_class.assert_called_once_with(self.praw_reddit, subreddit_inst, "some/page/name")
