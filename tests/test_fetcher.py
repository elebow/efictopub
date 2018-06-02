import pytest
from unittest.mock import MagicMock
from unittest.mock import patch


from app.fetcher import Fetcher


@pytest.fixture
def reddit_submissions(self, _url_or_id):
    return [
        MagicMock("Chapter", get_text=lambda: "chapter 1", created_utc="start_date", permalink="permalink",
                  author_name="great-author"),
        MagicMock("Chapter", get_text=lambda: "chapter 2"),
        MagicMock("Chapter", get_text=lambda: "chapter 3", created_utc="end_date")
    ]


class TestFetcher:

    def setup_method(self):
        self.subject = Fetcher()

    @patch("app.fetchers.Reddit.submissions_following_next_links", reddit_submissions)
    @patch("app.archive.Archive.store")
    def test_fetch_from_reddit_next(self, archive):
        story = self.subject.fetch_from_reddit_next("_whatever-url-or-id")

        assert [chap.get_text() for chap in story.chapters] == ["chapter 1", "chapter 2", "chapter 3"]
        assert story.author == "great-author"
        assert story.date_start == "start_date"
        assert story.date_end == "end_date"
