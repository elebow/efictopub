import os
import yaml


class Archive:
    """Saves and retrieves copies of stories on disk."""

    @staticmethod
    def get(id):
        # TODO accept partial ids, as long as they map to a unique file
        with open(Archive.path(id), "r") as infile:
            return yaml.safe_load(infile)

    @staticmethod
    def store(id, story):
        with open(Archive.path(id), "w") as outfile:
            return yaml.dump(story, outfile)

    @staticmethod
    def path(id):
        return f"{os.environ.get('HOME')}/.reddit_series/cache/{id}.yml"  # TODO make configurable
