import pytest

from app.models import reddit


@pytest.fixture()
def praw_submissions():
    import pickle
    with open("tests/fixtures/array_of_3_submissions_with_comments.pickle", "rb") as file:
        return pickle.load(file)


class TestComment:

    def setup_method(self):
        self.comments = [reddit.Comment(c) for c in praw_submissions()[0].comments]

    def test_all_links_mentioned_in_comment(self, praw_submissions):
        links = self.comments[7].all_links_in_text()
        assert links[3].text == '[OC] Human-Standard.'
