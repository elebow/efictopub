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
    def store(story):
        with open(Archive.path(story.id), "w") as outfile:
            return yaml.dump(story, outfile)

    @staticmethod
    def path(id):
        return f"{os.environ.get('HOME')}/.series-to-epub/cache/{id}.yml"  # TODO make configurable
