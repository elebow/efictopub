from efictopub import config
from efictopub.models.reddit import RedditSubmission

import pytest


class TestRedditSubmission:
    @pytest.fixture(autouse=True)
    def base_config(self):
        config.config["fetch_comments"] = True

    def test_comments(self, praw_submission):
        submission = RedditSubmission(praw_submission)
        comments = submission.comments

        assert len(comments) == 2
        assert comments[0].author == "Redditor Name (Author Flair Text)"

    def test_init(self, praw_submission):
        submission = RedditSubmission(praw_submission)

        assert submission.ups == 5
        assert len(submission.comments) == 2
        assert len(submission.comments[1].replies) == 2
        assert len(submission.comments[1].replies[0].replies) == 0

    def test_extract_text_submission(self, praw_submission):
        chapter = RedditSubmission(praw_submission)

        assert chapter.text == "<p>selftext HTML</p>"

    def test_extract_text_submission_note(self, praw_submission, praw_comment):
        comment_with_author_note = praw_comment
        comment_with_author_note.body_html = "short author note"
        praw_submission.comments.__iter__.return_value = [
            comment_with_author_note,
            praw_comment,
        ]
        chapter = RedditSubmission(praw_submission)

        assert chapter.text == "<p>selftext HTML</p>"
        assert chapter.comments[0].text == "<p>short author note</p>"

    def test_extract_text_submission_continued(self, praw_submission, praw_comment):
        comment_continuation = praw_comment
        comment_continuation.body_html = "long continuation 1" * 200
        comment_continuation.replies[0].body_html = "long continuation 2" * 200
        praw_submission.comments.__iter__.return_value = [
            comment_continuation,
            praw_comment,
        ]
        chapter = RedditSubmission(praw_submission)

        assert chapter.text == (
            "<p>selftext HTML</p>\n"
            + "\n"
            + "<p>"
            + "long continuation 1" * 200
            + "</p>\n\n"
            + "<p>"
            + "long continuation 2" * 200
            + "</p>"
        )
        assert chapter.comments[0].text == "[efictopub]: included in chapter text"
        assert (
            chapter.comments[0].replies[0].text
            == "[efictopub]: included in chapter text"
        )
