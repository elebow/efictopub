from unittest import TestCase
from unittest.mock import MagicMock
from unittest.mock import patch


from app.main import Main

from tests.fixtures.doubles import chapters_double


class TestMain:

    @patch("app.fetchers.RedditNext.fetch_chapters", lambda _x: chapters_double(3))
    @patch("app.archive.store")
    def test_fetch_from_reddit_next(self, archive):
        args = MagicMock(fetcher="RedditNext", target="_whatever-url-or-id")
        subject = Main(args)
        story = subject.get_story()

        assert [chap.text for chap in story.chapters] == \
            ["chapter content 0", "chapter content 1", "chapter content 2"]
        assert story.author_name == "great author 0"

    def test__fetcher_names(self):
        TestCase().assertCountEqual(Main._fetcher_names(),
                                    ["Archive", "FFNet", "RedditNext", "RedditAuthor", "RedditMentions"])
