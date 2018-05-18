import pytest
from unittest.mock import MagicMock
from unittest.mock import patch

from app.submission import Submission

@pytest.fixture()
def praw_submissions():
    import pickle
    with open("tests/fixtures/array_of_3_submissions_with_comments.pickle", "rb") as file:
        return pickle.load(file)


class TestSubmission(object):

    def praw_reddit(self):
        return MagicMock(redditor='some_redditor')

    def mock_reddit_new_submission(self, url=None, id=None):
        if url is not None:
            return [subm for subm in praw_submissions() if subm.url == url][0]
        elif id is not None:
            return [subm for subm in praw_submissions() if subm.id == id][0]

    def setup_method(self):
        self.submissions = [Submission(s) for s in praw_submissions()]

    @patch("praw.models.Submission", mock_reddit_new_submission)
    def test_all_comments_for_submission(self, praw_submissions):
        comments = self.submissions[0].comments
        assert len(comments) == 9
        assert comments[0].replies[0].author_name == "WTMAWLR"

    def test_extract_subm_attrs(self, praw_submissions):
        submission = self.submissions[1]
        assert submission.ups == 49
        assert len(submission.comments) == 4
        assert len(submission.comments[1].replies) == 1
        assert len(submission.comments[1].replies[0].replies) == 1
        assert len(submission.comments[1].replies[0].replies[0].replies) == 0
