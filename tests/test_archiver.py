import os


from app.archiver import Archiver


class TestArchiver:

    def setup_class(self):
        self.key = "55555-my-great-story-key"

    def setup_method(self):
        self.subject = Archiver(self.key)

    def test_calculate_path(self):
        assert self.subject.calculate_path() == f"{os.environ.get('HOME')}/.reddit_series/cache/55555-my-great-story-key.yml"
