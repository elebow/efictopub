import pytest
from unittest.mock import MagicMock
from unittest.mock import patch

from efictopub.lib import reddit_util
from efictopub.models.reddit import RedditSubmission, RedditComment, RedditWikiPage
from efictopub import exceptions


subreddit_inst = MagicMock()
subreddit_class = MagicMock(return_value=subreddit_inst)


class TestRedditUtil:
    def setup_method(self):
        self.subject = reddit_util
        self.praw_reddit = MagicMock()

    def test_redditor_name_from_url(self):
        assert (
            self.subject.redditor_name_from_url("reddit.com/u/redditor1") == "redditor1"
        )
        assert (
            self.subject.redditor_name_from_url("www.reddit.com/u/redditor1")
            == "redditor1"
        )
        assert (
            self.subject.redditor_name_from_url("http://reddit.com/u/redditor1")
            == "redditor1"
        )
        assert (
            self.subject.redditor_name_from_url("https://www.reddit.com/u/redditor1")
            == "redditor1"
        )

    @patch("efictopub.lib.reddit_util.parse_url")
    def test_parse_id_or_url_submission(self, parse_url):
        submission_url = "https://www.reddit.com/r/great_subr/comments/000/great_subm"
        self.subject.parse_id_or_url(submission_url, self.praw_reddit)
        self.subject.parse_url.assert_called_once_with(submission_url, self.praw_reddit)

    @patch("efictopub.lib.reddit_util.parse_url")
    def test_parse_id_or_url_comment(self, parse_url):
        comment_url = "https://www.reddit.com/r/great_subr/comments/000/great_subm/999"
        self.subject.parse_id_or_url(comment_url, self.praw_reddit)
        self.subject.parse_url.assert_called_once_with(comment_url, self.praw_reddit)

    @patch("efictopub.lib.reddit_util.parse_url")
    def test_parse_id_or_url_wikipage(self, parse_url):
        wikipage_url = "reddit.com/r/whatever/wiki/pagename"
        self.subject.parse_id_or_url(wikipage_url, self.praw_reddit)
        self.subject.parse_url.assert_called_once_with(wikipage_url, self.praw_reddit)

    @patch("efictopub.lib.reddit_util.parse_url")
    def test_parse_id_or_url_ambiguous(self, parse_url):
        # ambiguous id
        with pytest.raises(exceptions.AmbiguousIdError):
            self.subject.parse_id_or_url("aaaaaa", self.praw_reddit)

    @patch("praw.models.Submission")
    @patch("praw.models.Comment")
    @patch("praw.models.WikiPage")
    @patch("praw.models.Subreddit", subreddit_class)
    def test_parse_url(self, wikipage_class, comment_class, submission_class):
        submission_url = (
            "https://reddit.com/r/my_great_subreddit/comments/a123/my_great_title/"
        )
        comment_url = (
            "https://reddit.com/r/my_great_subreddit/comments/a123/my_great_title/b456/"
        )
        wiki_url = "https://reddit.com/r/my_great_subreddit/wiki/some/page/name"

        result = self.subject.parse_url(submission_url, self.praw_reddit)
        assert isinstance(result, RedditSubmission)
        submission_class.assert_called_once_with(self.praw_reddit, url=submission_url)

        result = self.subject.parse_url(comment_url, self.praw_reddit)
        assert isinstance(result, RedditComment)
        comment_class.assert_called_once_with(self.praw_reddit, url=comment_url)

        result = self.subject.parse_url(wiki_url, self.praw_reddit)
        assert isinstance(result, RedditWikiPage)
        subreddit_class.assert_called_once_with(self.praw_reddit, "my_great_subreddit")
        wikipage_class.assert_called_once_with(
            self.praw_reddit, subreddit_inst, "some/page/name"
        )
