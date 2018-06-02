import praw
import pytest
from unittest.mock import MagicMock

from app.models import reddit


@pytest.fixture()
def praw_submissions():
    import pickle
    with open("tests/fixtures/array_of_3_submissions_with_comments.pickle", "rb") as file:
        return pickle.load(file)


@pytest.fixture
def submission_alone():
    return MagicMock(selftext="aaa")


@pytest.fixture
def submission_author_note():
    comment = MagicMock(body="short author note")
    praw_submission = MagicMock(selftext="aaa")
    comment_forest = praw.models.comment_forest.CommentForest(praw_submission, [comment])
    praw_submission.comments = comment_forest
    return praw_submission


@pytest.fixture
def submission_continued_in_comments():
    comment2 = MagicMock(body="long continuation 2" * 200)
    comment1 = MagicMock(body="long continuation 1" * 200, replies=[comment2])
    praw_submission = MagicMock(selftext="aaa")
    comment_forest = praw.models.comment_forest.CommentForest(praw_submission, [comment1])
    praw_submission.comments = comment_forest
    return praw_submission


class TestSubmission:

    def setup_method(self):
        self.submissions = [reddit.Submission(s) for s in praw_submissions()]

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

    def test_extract_text_submission(self, submission_alone):
        chapter = reddit.Submission(submission_alone)
        assert chapter.get_text() == "aaa"

    def test_extract_text_submission_note(self, submission_author_note):
        chapter = reddit.Submission(submission_author_note)
        assert chapter.get_text() == "aaa"
        assert chapter.comments[0].body == "short author note"

    def test_extract_text_submission_continued(self, submission_continued_in_comments):
        chapter = reddit.Submission(submission_continued_in_comments)
        assert chapter.get_text() == ("aaa" + "long continuation 1" * 200 + "long continuation 2" * 200)
        assert chapter.comments[0].body == "[series-to-epub]: included in chapter text"
        assert chapter.comments[0].replies[0].body == "[series-to-epub]: included in chapter text"
