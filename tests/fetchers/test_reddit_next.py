import pytest
from unittest.mock import patch

from app import fetchers
from app import exceptions

from tests.fixtures.doubles import praw_submission_with_ambiguous_next
from tests.fixtures.real import praw_submissions_real, find_praw_submission_real


class TestFetchersRedditNext:
    @patch("praw.models.Submission", find_praw_submission_real)
    def test_submissions_following_next_links(self):
        subms = fetchers.RedditNext(praw_submissions_real()[0]).fetch_chapters()

        assert [subm.permalink for subm in subms] == [
            "/r/HFY/comments/886al5/oc_falling_sky/",
            "/r/HFY/comments/88bcar/oc_falling_sky01warm_reception/",
            "/r/HFY/comments/88ejcl/oc_falling_sky02ships_alight/"]

    def test_ambiguous_next(self):
        with pytest.raises(exceptions.AmbiguousNextError):
            [subm
             for subm
             in fetchers.RedditNext("_what").generate_next_submissions(praw_submission_with_ambiguous_next())]
