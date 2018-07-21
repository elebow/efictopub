import pytest
from unittest.mock import patch

from app import fetchers
from app import exceptions

from tests.fixtures.doubles import praw_submission_with_ambiguous_next
from tests.fixtures.doubles import praw_submissions
from tests.fixtures.doubles import find_praw_submission


class TestFetchersRedditNext:
    @patch("praw.models.Submission", find_praw_submission)
    def test_submissions_following_next_links(self):
        subms = fetchers.RedditNext(praw_submissions[0].permalink).fetch_chapters()

        assert [subm.permalink for subm in subms] == [
            "https://www.reddit.com/r/great_subreddit/comments/000000/great_title",
            "https://www.reddit.com/r/great_subreddit/comments/000001/great_title",
            "https://www.reddit.com/r/great_subreddit/comments/000002/great_title"]

    def test_ambiguous_next(self):
        with pytest.raises(exceptions.AmbiguousNextError):
            [subm
             for subm
             in fetchers.RedditNext("_what").generate_next_submissions(praw_submission_with_ambiguous_next())]
