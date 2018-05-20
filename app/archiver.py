import os
import yaml


class Archiver:
    """Saves and retrieves copies of stories on disk."""

    def __init__(self, key):
        self.key = key
        self.path = self.calculate_path()

    def get(key):
        with open(self.path, "r") as infile:
            return yaml.safe_load(infile)

    def store(self, book):
        with open(self.path, "w") as outfile:
            return yaml.dump(book, outfile)

    def calculate_path(self):
        return f"{os.environ.get('HOME')}/.reddit_series/cache/{self.key}.yml"  # TODO make configurable
