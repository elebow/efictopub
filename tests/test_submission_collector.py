import pytest
from unittest.mock import MagicMock

from app.submission_collector import SubmissionCollector


class TestSubmissionCollector:

    @pytest.fixture
    def praw_submissions(self):
        import pickle
        with open("tests/fixtures/array_of_3_submissions_with_comments.pickle", "rb") as file:
            return pickle.load(file)

    @pytest.fixture
    def praw_redditor(self):
        return MagicMock(name='some_redditor',
                         submissions=praw_submissions())

    def praw_reddit(self):
        return MagicMock(redditor='some_redditor')

    def setup_class(self):
        # don't actually hit reddit
        SubmissionCollector.setup_reddit = MagicMock()

    def setup_method(self):
        self.submission_collector = SubmissionCollector(app="", secret="", user_agent="")

    def test_all_comments_for_submission(self):
        comments = self.submission_collector.all_comments_for_submission(self.praw_submissions()[0])
        assert len(comments) == 25
        assert comments[1].replies[2].author_name == "illiesfw"

    def test_extract_subm_attrs(self):
        submission = self.submission_collector.extract_subm_attrs(self.praw_submissions()[1])
        assert submission.ups == 906
        assert len(submission.comments) == 24
        assert len(submission.comments[2].replies) == 3
        assert len(submission.comments[2].replies[1].replies) == 2
        assert len(submission.comments[2].replies[1].replies[0].replies) == 0
