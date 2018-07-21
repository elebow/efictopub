from app.models import reddit

from tests.fixtures.doubles import praw_submissions


class TestComment:

    def setup_method(self):
        self.comments = [reddit.Comment(c) for c in praw_submissions[0].comments]

    def test_all_links_mentioned_in_comment(self):
        links = self.comments[2].all_links_in_text()
        assert links[0].text == "some link"
