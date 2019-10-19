import pytest

from efictopub.lib import reddit_util
from efictopub.models.reddit import RedditSubmission, RedditComment, RedditWikiPage
from efictopub import exceptions


class TestRedditUtil:
    def test_redditor_name_from_url(self):
        assert (
            reddit_util.redditor_name_from_url("reddit.com/u/redditor1") == "redditor1"
        )
        assert (
            reddit_util.redditor_name_from_url("www.reddit.com/u/redditor1")
            == "redditor1"
        )
        assert (
            reddit_util.redditor_name_from_url("http://reddit.com/u/redditor1")
            == "redditor1"
        )
        assert (
            reddit_util.redditor_name_from_url("https://www.reddit.com/u/redditor1")
            == "redditor1"
        )

    def test_parse_id_or_url_submission(self, mocker):
        mocker.patch("efictopub.lib.reddit_util.parse_url")

        submission_url = "https://www.reddit.com/r/great_subr/comments/000/great_subm"
        reddit_util.parse_id_or_url(submission_url, "praw_reddit object")

        reddit_util.parse_url.assert_called_once_with(submission_url, mocker.ANY)

    def test_parse_id_or_url_comment(self, mocker):
        mocker.patch("efictopub.lib.reddit_util.parse_url")

        comment_url = "https://www.reddit.com/r/great_subr/comments/000/great_subm/999"
        reddit_util.parse_id_or_url(comment_url, "praw_reddit object")

        reddit_util.parse_url.assert_called_once_with(comment_url, mocker.ANY)

    def test_parse_id_or_url_wikipage(self, mocker):
        mocker.patch("efictopub.lib.reddit_util.parse_url")

        wikipage_url = "reddit.com/r/whatever/wiki/pagename"
        reddit_util.parse_id_or_url(wikipage_url, "praw_reddit object")

        reddit_util.parse_url.assert_called_once_with(wikipage_url, mocker.ANY)

    def test_parse_id_or_url_ambiguous(self, mocker):
        mocker.patch("efictopub.lib.reddit_util.parse_url")

        with pytest.raises(exceptions.AmbiguousIdError):
            reddit_util.parse_id_or_url("aaaaaa", "praw_reddit object")

    def test_parse_url(self, mocker):
        praw_submission_class = mocker.patch("praw.models.Submission")
        praw_comment_class = mocker.patch("praw.models.Comment")
        praw_wikipage_class = mocker.patch("praw.models.WikiPage")
        praw_subreddit_class = mocker.patch("praw.models.Subreddit")

        submission_url = (
            "https://reddit.com/r/my_great_subreddit/comments/a123/my_great_title/"
        )
        comment_url = (
            "https://reddit.com/r/my_great_subreddit/comments/a123/my_great_title/b456/"
        )
        wiki_url = "https://reddit.com/r/my_great_subreddit/wiki/some/page/name"

        result = reddit_util.parse_url(submission_url, "praw_reddit object")
        assert isinstance(result, RedditSubmission)
        praw_submission_class.assert_called_once_with(mocker.ANY, url=submission_url)

        result = reddit_util.parse_url(comment_url, "praw_reddit object")
        assert isinstance(result, RedditComment)
        praw_comment_class.assert_called_once_with(mocker.ANY, url=comment_url)

        result = reddit_util.parse_url(wiki_url, "praw_reddit object")
        assert isinstance(result, RedditWikiPage)
        praw_subreddit_class.assert_called_once_with(mocker.ANY, "my_great_subreddit")
        praw_wikipage_class.assert_called_once_with(
            mocker.ANY, praw_subreddit_class(), "some/page/name"
        )
