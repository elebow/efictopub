import pytest
from unittest.mock import MagicMock
from unittest.mock import patch
from unittest import mock

from app import fetchers
from app.models import reddit
from app import exceptions


@pytest.fixture
def praw_submissions():
    import pickle
    with open("tests/fixtures/array_of_3_submissions_with_comments.pickle", "rb") as file:
        return pickle.load(file)


@pytest.fixture
def submission_with_ambiguous_next():
    return MagicMock("praw.models.Submission", selftext="[next](link1) [next](link2)")


@pytest.fixture
def praw_redditor(_name):
    return MagicMock(name='some_redditor',
                     submissions=MagicMock(new=praw_submissions))


@pytest.fixture
def mock_reddit_new_submission(self, url=None, id=None):
    if url is not None:
        return [subm for subm in praw_submissions() if subm.url == url][0]
    elif id is not None:
        return [subm for subm in praw_submissions() if subm.id == id][0]


class TestFetchersRedditMentions:
    @patch("praw.models.Submission", mock_reddit_new_submission)
    def test_submissions_in_list_of_ids(self, praw_submissions):
        ids = ["886al5", "88bcar", "88ejcl"]
        subms = fetchers.RedditMentions().submissions_in_list_of_ids(ids)

        assert [subm.reddit_id for subm in subms] == ["886al5", "88bcar", "88ejcl"]
