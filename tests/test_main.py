import pytest
from unittest import TestCase
from unittest.mock import MagicMock
from unittest.mock import patch


from app.main import Main


@pytest.fixture
def reddit_submissions(_url_or_id):
    return [
        MagicMock("Chapter", get_text=lambda: "chapter 1", created_utc="start_date", permalink="permalink",
                  author_name="great-author"),
        MagicMock("Chapter", get_text=lambda: "chapter 2"),
        MagicMock("Chapter", get_text=lambda: "chapter 3", created_utc="end_date")
    ]


class TestMain:

    @patch("app.fetchers.RedditNext.fetch_chapters", reddit_submissions)
    @patch("app.archive.Archive.store")
    def test_fetch_from_reddit_next(self, archive):
        args = MagicMock(fetcher="RedditNext", target="_whatever-url-or-id")
        subject = Main(args)
        story = subject.get_story()

        assert [chap.get_text() for chap in story.chapters] == ["chapter 1", "chapter 2", "chapter 3"]
        assert story.author_name == "great-author"
        assert story.date_start == "start_date"
        assert story.date_end == "end_date"

    def test__fetcher_names(self):
        TestCase().assertCountEqual(Main._fetcher_names(),
                                    ["Archive", "RedditNext", "RedditAuthor", "RedditMentions"])
