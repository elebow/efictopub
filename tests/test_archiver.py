import os


from app.archive import Archive


class TestArchiver:

    def setup_class(self):
        self.key = "55555-my-great-story-key"

    def setup_method(self):
        self.subject = Archive()

    def test_path(self):
        assert self.subject.path(self.key) == f"{os.environ.get('HOME')}/.reddit_series/cache/55555-my-great-story-key.yml"
