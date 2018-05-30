import pytest

from app.models.reddit.submission import Submission


@pytest.fixture()
def praw_submissions():
    import pickle
    with open("tests/fixtures/array_of_3_submissions_with_comments.pickle", "rb") as file:
        return pickle.load(file)


class TestSubmission(object):

    def setup_method(self):
        self.submissions = [Submission(s) for s in praw_submissions()]

    def test_comments(self, praw_submissions):
        comments = self.submissions[0].comments
        assert len(comments) == 9
        assert comments[0].replies[0].author_name == "WTMAWLR"

    def test_init(self, praw_submissions):
        submission = self.submissions[1]
        assert submission.ups == 49
        assert len(submission.comments) == 4
        assert len(submission.comments[1].replies) == 1
        assert len(submission.comments[1].replies[0].replies) == 1
        assert len(submission.comments[1].replies[0].replies[0].replies) == 0

    def test_all_links_in_text(self, praw_submissions):
        links = self.submissions[0].all_links_in_text()
        assert links[0].text == '[Next Part]'
