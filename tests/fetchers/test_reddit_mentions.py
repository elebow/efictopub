from unittest.mock import patch

from app import fetchers

from tests.fixtures.real import find_praw_submission_real


class TestFetchersRedditMentions:
    @patch("praw.models.Submission", find_praw_submission_real)
    def test_submissions_in_list_of_ids(self):
        ids = ["886al5", "88bcar", "88ejcl"]
        subms = fetchers.RedditMentions().submissions_in_list_of_ids(ids)

        assert [subm.reddit_id for subm in subms] == ["886al5", "88bcar", "88ejcl"]
