import pytest
from unittest.mock import patch
from unittest.mock import MagicMock

from app.config import config
from app.fetchers import reddit_next
from app import exceptions

from tests.fixtures.doubles import praw_submission_with_ambiguous_next
from tests.fixtures.doubles import praw_submission_with_duplicate_next
from tests.fixtures.doubles import praw_submissions
from tests.fixtures.doubles import find_praw_submission


class TestFetchersRedditNext:
    @patch("praw.models.Submission", find_praw_submission)
    def test_submissions_following_next_links(self):
        subms = reddit_next.Fetcher(praw_submissions[0].permalink).fetch_chapters()

        assert [subm.permalink for subm in subms] == [
            "https://www.reddit.com/r/great_subreddit/comments/000000/great_title",
            "https://www.reddit.com/r/great_subreddit/comments/000001/great_title",
            "https://www.reddit.com/r/great_subreddit/comments/000002/great_title",
        ]

    def test_ambiguous_next(self):
        with pytest.raises(exceptions.AmbiguousNextError):
            [
                subm
                for subm in reddit_next.Fetcher("_what").generate_next_submissions(
                    praw_submission_with_ambiguous_next()
                )
            ]

    @patch("praw.models.Submission", find_praw_submission)
    def test_duplicate_next(self):
        [
            subm
            for subm in reddit_next.Fetcher("_what").generate_next_submissions(
                praw_submission_with_duplicate_next()
            )
        ]

    @patch("praw.models.Submission", find_praw_submission)
    def test_skip_comments(self):
        # TODO rename this test. It's not skipping comments.
        config["fetch_comments"] = True
        chapters = reddit_next.Fetcher(praw_submissions[0].permalink).fetch_chapters()
        assert [len(chapter.comments) for chapter in chapters] == [3, 4, 5]
