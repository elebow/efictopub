from doubles import allow

from app import fetchers

from tests.fixtures.doubles import praw_redditor_with_submissions_double


class TestFetchersRedditAuthor:
    def test_submissions_by_author(self):
        fetcher = fetchers.RedditAuthor(author_name="some redditor")
        allow(fetcher.reddit).redditor.and_return(praw_redditor_with_submissions_double())

        subms = fetcher.fetch_chapters()
        assert [subm.reddit_id for subm in subms] == ["000000", "000001", "000002"]

    def test_submissions_by_author_with_pattern(self):
        fetcher = fetchers.RedditAuthor(author_name="some redditor", pattern=r"0\d")
        allow(fetcher.reddit).redditor.and_return(praw_redditor_with_submissions_double())

        subms = fetcher.fetch_chapters()
        assert [subm.reddit_id for subm in subms] == ["000001", "000002"]
