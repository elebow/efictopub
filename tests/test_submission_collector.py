import pytest
from unittest.mock import MagicMock
from unittest.mock import patch

from app.submission_collector import SubmissionCollector


@pytest.fixture()
def praw_submissions():
    import pickle
    with open("tests/fixtures/array_of_3_submissions_with_comments.pickle", "rb") as file:
        return pickle.load(file)


@pytest.fixture
def praw_redditor():
    return MagicMock(name='some_redditor', submissions=praw_submissions)


class TestSubmissionCollector(object):

    def praw_reddit(self):
        return MagicMock(redditor='some_redditor')

    def setup_class(self):
        # don't actually hit reddit
        SubmissionCollector.setup_reddit = MagicMock()
        SubmissionCollector.reddit = MagicMock()

    def mock_reddit_new_submission_from_url(self, url):
        return [subm for subm in praw_submissions() if subm.url == url][0]

    def setup_method(self):
        self.submission_collector = SubmissionCollector(app="", secret="", user_agent="")

    @patch("praw.models.Submission", mock_reddit_new_submission_from_url)
    def test_all_submissions_following_next_links(self, praw_submissions):
        subms = self.submission_collector.all_submissions_following_next_links(praw_submissions[0])

        assert len(subms) == 3
        assert subms[0].reddit_id == "886al5"
        assert subms[1].reddit_id == "88bcar"
        assert subms[2].reddit_id == "88ejcl"

    def test_all_comments_for_submission(self, praw_submissions):
        comments = self.submission_collector.all_comments_for_submission(praw_submissions[0])
        assert len(comments) == 9
        assert comments[0].replies[0].author_name == "WTMAWLR"

    def test_extract_subm_attrs(self, praw_submissions):
        submission = self.submission_collector.extract_subm_attrs(praw_submissions[1])
        assert submission.ups == 49
        assert len(submission.comments) == 4
        assert len(submission.comments[1].replies) == 1
        assert len(submission.comments[1].replies[0].replies) == 1
        assert len(submission.comments[1].replies[0].replies[0].replies) == 0
