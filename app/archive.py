import os
import yaml


class Archive:
    """Saves and retrieves copies of stories on disk."""

    @staticmethod
    def get(key):
        with open(path(key), "r") as infile:
            return yaml.safe_load(infile)

    @staticmethod
    def store(key, story):
        with open(path(key), "w") as outfile:
            return yaml.dump(story, outfile)

    @staticmethod
    def path(key):
        return f"{os.environ.get('HOME')}/.reddit_series/cache/{key}.yml"  # TODO make configurable
