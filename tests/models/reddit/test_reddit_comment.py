from app.models.reddit import RedditComment

from tests.fixtures.doubles import praw_submissions


class TestRedditComment:
    def setup_method(self):
        self.reddit_comments = [RedditComment(c) for c in praw_submissions[0].comments]

    def test_all_links_mentioned_in_comment(self):
        links = self.reddit_comments[2].all_links_in_text()
        assert links[0].text == "some link"

    def test_as_comment(self):
        comments = [reddit_comment.as_comment() for reddit_comment in self.reddit_comments]

        assert [comment.author for comment in comments] == ["redditor 0", "redditor 0", "redditor 0"]
        assert [comment.date_published for comment in comments] == [
            "created utc 0",
            "created utc 1",
            "created utc 2",
        ]
        assert [comment.date_updated for comment in comments] == [
            "edited timestamp 0",
            "edited timestamp 1",
            "edited timestamp 2",
        ]
        assert [comment.replies for comment in comments] == [[], [], []]  # TODO make these nontrivial
