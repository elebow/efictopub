from doubles import allow

from efictopub import config
from efictopub.fetchers import reddit_author

from tests.fixtures.real import get_reddit_submission


class TestFetchersRedditAuthor:
    def test_submissions_by_author(self, mocker):
        mock_praw_submissions = [
            mocker.Mock(title="PRAW Submission 00", id="000000"),
            mocker.Mock(title="PRAW Submission 01", id="000001"),
            mocker.Mock(title="PRAW Submission 02", id="000002"),
        ]
        mock_redditor = mocker.Mock(
            submissions=mocker.Mock(new=mocker.Mock(return_value=mock_praw_submissions))
        )
        mock_reddit = mocker.Mock(redditor=mocker.Mock(return_value=mock_redditor))
        mocker.patch("efictopub.lib.reddit_util.setup_reddit", return_value=mock_reddit)

        fetcher = reddit_author.Fetcher("reddit.com/u/some_redditor")
        subms = fetcher.fetch_submissions()

        assert [subm.reddit_id for subm in subms] == ["000000", "000001", "000002"]

    def test_submissions_by_author_with_pattern(self, mocker):
        mock_praw_submissions = [
            mocker.Mock(title="PRAW Submission 00", id="000000"),
            mocker.Mock(title="PRAW Submission 01", id="000001"),
            mocker.Mock(title="PRAW Submission 02", id="000002"),
        ]
        mock_redditor = mocker.Mock(
            submissions=mocker.Mock(new=mocker.Mock(return_value=mock_praw_submissions))
        )
        mock_reddit = mocker.Mock(redditor=mocker.Mock(return_value=mock_redditor))
        mocker.patch("efictopub.lib.reddit_util.setup_reddit", return_value=mock_reddit)
        config.config["fetcher_opts"] = ["title_pattern=[^0]\\Z"]

        fetcher = reddit_author.Fetcher("reddit.com/u/some_redditor")
        subms = fetcher.fetch_submissions()

        assert [subm.reddit_id for subm in subms] == ["000001", "000002"]
