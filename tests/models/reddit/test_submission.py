from app.models import reddit

from tests.fixtures.doubles import praw_submission_double, \
    praw_submission_with_author_note_double, \
    praw_submission_continued_in_comments_double, \
    praw_submissions


class TestSubmission:
    def setup_method(self):
        self.submissions = [reddit.Submission(s) for s in praw_submissions]

    def test_comments(self):
        comments = self.submissions[0].comments
        assert len(comments) == 3
        assert comments[0].author == "redditor 0 ()"

    def test_init(self):
        submission = self.submissions[1]
        assert submission.ups == 5
        assert len(submission.comments) == 4
        assert len(submission.comments[1].replies) == 0

    def test_all_links_in_text(self):
        links = self.submissions[0].all_links_in_text()
        assert links[0].text == 'Next'

    def test_extract_text_submission(self):
        chapter = reddit.Submission(praw_submission_double())
        assert chapter.get_full_text() == "some selftext"

    def test_extract_text_submission_note(self):
        chapter = reddit.Submission(praw_submission_with_author_note_double())
        assert chapter.get_full_text() == "some selftext"
        assert chapter.comments[0].text == "<p>short author note</p>"

    def test_extract_text_submission_continued(self):
        chapter = reddit.Submission(praw_submission_continued_in_comments_double())
        assert chapter.get_full_text() == ("some selftext" + "\n\n" +
                                           "<p>" + "long continuation 1" * 200 + "</p>\n\n" +
                                           "<p>" + "long continuation 2" * 200 + "</p>")
        assert chapter.comments[0].text == "[efictopub]: included in chapter text"
        assert chapter.comments[0].replies[0].text == "[efictopub]: included in chapter text"
