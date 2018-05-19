import pytest
from unittest.mock import MagicMock

import praw

from app.chapter import Chapter
from app.submission import Submission


@pytest.fixture
def submission_alone():
    return Submission(MagicMock(selftext="aaa"))


@pytest.fixture
def submission_author_note():
    comment = MagicMock(body="short author note")
    praw_submission = MagicMock(selftext="aaa")
    comment_forest = praw.models.comment_forest.CommentForest(praw_submission, [comment])
    praw_submission.comments = comment_forest
    return Submission(praw_submission)


@pytest.fixture
def submission_continued_in_comments():
    comment2 = MagicMock(body="long continuation 2" * 200)
    comment1 = MagicMock(body="long continuation 1" * 200, replies=[comment2])
    praw_submission = MagicMock(selftext="aaa")
    comment_forest = praw.models.comment_forest.CommentForest(praw_submission, [comment1])
    praw_submission.comments = comment_forest
    return Submission(praw_submission)


class TestChapter(object):

    def test_extract_text_submission(self, submission_alone):
        chapter = Chapter(submission_alone)
        assert chapter.extract_text() == "aaa"

    def test_extract_text_submission_note(self, submission_author_note):
        chapter = Chapter(submission_author_note)
        assert chapter.extract_text() == "aaa"

    def test_extract_text_submission_continued(self, submission_continued_in_comments):
        chapter = Chapter(submission_continued_in_comments)
        assert chapter.extract_text() == "aaa" + "long continuation 1" * 200 + "long continuation 2" * 200
