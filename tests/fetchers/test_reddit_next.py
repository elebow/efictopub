import pytest

from efictopub import config
from efictopub.fetchers import reddit_next
from efictopub import exceptions

from tests.fixtures import get_reddit_submission


class TestFetchersRedditNext:
    def test_submissions_following_next_links(self, mocker):
        mocker.patch("efictopub.lib.reddit_util.parse_url", get_reddit_submission)
        subms = reddit_next.Fetcher(
            "https://www.reddit.com/r/great_subreddit/comments/000000/next_links"
        ).fetch_submissions()

        assert [subm.permalink for subm in subms] == [
            "https://www.reddit.com/r/great_subreddit/comments/000000/next_links",
            "https://www.reddit.com/r/great_subreddit/comments/000001/next_links",
            "https://www.reddit.com/r/great_subreddit/comments/000002/next_links",
        ]

    def test_ambiguous_next(self, mocker):
        mocker.patch("efictopub.lib.reddit_util.parse_url", get_reddit_submission)
        with pytest.raises(exceptions.AmbiguousNextError):
            reddit_next.Fetcher(
                "https://www.reddit.com/r/great_subreddit/comments/000003/ambiguous_next"
            ).fetch_submissions()

    def test_duplicate_next(self, mocker):
        mocker.patch("efictopub.lib.reddit_util.parse_url", get_reddit_submission)
        subms = reddit_next.Fetcher(
            "https://www.reddit.com/r/great_subreddit/comments/000004/duplicate_next"
        ).fetch_submissions()

        # implied asertion that no AmbiguousNextError is raised
        [subm for subm in subms]

    def test_fetch_comments(self, mocker, reddit_submission_factory):
        mocker.patch("efictopub.models.reddit.reddit_comment.RedditComment.body_html")
        mocker.patch("efictopub.lib.reddit_util.parse_url", get_reddit_submission)
        config.config["comments"] = "all"

        subms = reddit_next.Fetcher(
            "https://www.reddit.com/r/great_subreddit/comments/000005/has_comments"
        ).fetch_submissions()

        assert [len(subm.comments) for subm in subms] == [2]

    def test_skip_comments(self, mocker):
        mocker.patch("efictopub.models.reddit.reddit_comment.RedditComment.body_html")
        mocker.patch("efictopub.lib.reddit_util.parse_url", get_reddit_submission)
        config.config["comments"] = "none"

        subms = reddit_next.Fetcher(
            "https://www.reddit.com/r/great_subreddit/comments/000005/has_comments"
        ).fetch_submissions()

        assert [len(subm.comments) for subm in subms] == [0]
