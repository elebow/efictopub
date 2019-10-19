from efictopub import config
from efictopub.fetchers import reddit_author


class TestFetchersRedditAuthor:
    def test_submissions_by_author(self, mocker, redditor_with_submissions):
        mock_reddit = mocker.Mock(
            redditor=mocker.Mock(return_value=redditor_with_submissions)
        )
        mocker.patch("efictopub.lib.reddit_util.setup_reddit", return_value=mock_reddit)

        fetcher = reddit_author.Fetcher("reddit.com/u/some_redditor")
        subms = fetcher.fetch_submissions()

        assert [subm.reddit_id for subm in subms] == ["000000", "000001", "000002"]

    def test_submissions_by_author_with_pattern(
        self, mocker, redditor_with_submissions
    ):
        mock_reddit = mocker.Mock(
            redditor=mocker.Mock(return_value=redditor_with_submissions)
        )
        mocker.patch("efictopub.lib.reddit_util.setup_reddit", return_value=mock_reddit)
        config.config["fetcher_opts"] = ["title_pattern=[^0]\\Z"]

        fetcher = reddit_author.Fetcher("reddit.com/u/some_redditor")
        subms = fetcher.fetch_submissions()

        assert [subm.reddit_id for subm in subms] == ["000001", "000002"]
