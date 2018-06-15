from app.models import reddit

from tests.fixtures.real import praw_submissions_real


class TestComment:

    def setup_method(self):
        self.comments = [reddit.Comment(c) for c in praw_submissions_real()[0].comments]

    def test_all_links_mentioned_in_comment(self):
        links = self.comments[7].all_links_in_text()
        assert links[3].text == '[OC] Human-Standard.'
