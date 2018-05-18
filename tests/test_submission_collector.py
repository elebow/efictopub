import pytest
from unittest.mock import MagicMock
from unittest.mock import patch
from unittest import mock

from app.submission_collector import SubmissionCollector
from app.submission import Submission
from app.comment import Comment
from app import exceptions


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

    def mock_reddit_new_submission(self, url=None, id=None):
        if url is not None:
            return [subm for subm in praw_submissions() if subm.url == url][0]
        elif id is not None:
            return [subm for subm in praw_submissions() if subm.id == id][0]

    def setup_method(self):
        self.subject = SubmissionCollector(app="", secret="", user_agent="")

    @patch("praw.models.Submission", mock_reddit_new_submission)
    def test_all_submissions_in_list_of_ids(self, praw_submissions):
        ids = ["886al5", "88bcar", "88ejcl"]
        subms = self.subject.all_submissions_in_list_of_ids(ids)

        assert [subm.reddit_id for subm in subms] == ["886al5", "88bcar", "88ejcl"]

    @patch("praw.models.Submission", mock_reddit_new_submission)
    def test_all_submissions_following_next_links(self, praw_submissions):
        subms = self.subject.all_submissions_following_next_links(praw_submissions[0])

        assert [subm.reddit_id for subm in subms] == ["886al5", "88bcar", "88ejcl"]

    def test_parse_thing_or_id_or_url(self, praw_submissions):

        output_praw_subm = self.subject.parse_thing_or_id_or_url(praw_submissions[0])
        assert isinstance(output_praw_subm, Submission)
        assert len(output_praw_subm.comments) == len(praw_submissions[0].comments)

        output_praw_comm = self.subject.parse_thing_or_id_or_url(praw_submissions[0].comments[0])
        assert isinstance(output_praw_comm, Comment)

        #output_praw_wiki = self.subject.parse_thing_or_id_or_url(praw_submissions[0].comments[0])
        #assert isinstance(output_praw_wiki, WikiPage) #TODO

        with pytest.raises(exceptions.AmbiguousIdError):
            self.subject.parse_thing_or_id_or_url('aaaaaa')

        self.subject.parse_url = MagicMock()
        self.subject.parse_thing_or_id_or_url('https://whatever')
        self.subject.parse_url.assert_called_once_with('https://whatever')

    @patch("praw.models.Submission")
    @patch("praw.models.Comment")
    #@patch("app.subject.WikiPage") #TODO
    def test_parse_url(self, comment_class, submission_class):
        submission_url = 'https://reddit.com/r/my_great_subreddit/comments/a123/my_great_title/'
        comment_url = 'https://reddit.com/r/my_great_subreddit/comments/a123/my_great_title/b456/'

        self.subject.parse_url(submission_url)
        submission_class.assert_called_once_with(mock.ANY, url=submission_url)

        self.subject.parse_url(comment_url)
        comment_class.assert_called_once_with(mock.ANY, url=comment_url)
