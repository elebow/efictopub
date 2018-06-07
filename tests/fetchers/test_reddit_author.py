import pytest
from unittest.mock import MagicMock

from app import fetchers


@pytest.fixture
def praw_submissions():
    import pickle
    with open("tests/fixtures/array_of_3_submissions_with_comments.pickle", "rb") as file:
        return pickle.load(file)


@pytest.fixture
def praw_redditor(_name):
    return MagicMock(name='some_redditor',
                     submissions=MagicMock(new=praw_submissions))


class TestFetchersRedditAuthor:
    def test_submissions_by_author(self):
        fetcher = fetchers.RedditAuthor(author_name="WeirdSpecter")
        fetcher.reddit = MagicMock(redditor=praw_redditor)  # TODO use proper @patch decorator

        subms = fetcher.fetch_chapters()
        assert [subm.reddit_id for subm in subms] == ["886al5", "88bcar", "88ejcl"]

    def test_submissions_by_author_with_pattern(self):
        fetcher = fetchers.RedditAuthor(author_name="WeirdSpecter", pattern=r"0\d")
        fetcher.reddit = MagicMock(redditor=praw_redditor)  # TODO use proper @patch decorator

        subms = fetcher.fetch_chapters()
        assert [subm.reddit_id for subm in subms] == ["88bcar", "88ejcl"]
