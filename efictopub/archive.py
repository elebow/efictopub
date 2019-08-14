import glob
from pathlib import Path
import jsonpickle

from efictopub import config
from efictopub.exceptions import NoArchivedStoryError, AmbiguousArchiveIdError


"""Saves and retrieves copies of stories on disk."""


def get(id_or_path):
    with open(id_or_path_to_path(id_or_path), "r") as infile:
        return jsonpickle.decode(infile.read())


def store(story):
    path = path_for_story(story)
    with open(path, "w") as outfile:
        return outfile.write(jsonpickle.encode(story))


def path_for_story(story):
    return f"{config.get('archive_location')}/{story.id}.json"


def id_or_path_to_path(id_or_path):
    archive_file = Path(id_or_path)
    if archive_file.is_file():
        # id_or_path is already a path. Or the user is very unlucky.
        return id_or_path

    candidates = glob.glob(f"{config.get('archive_location')}/{id_or_path}*")
    num_candidates = len(candidates)
    if num_candidates == 0:
        raise NoArchivedStoryError(id_or_path)
    elif num_candidates == 1:
        return candidates[0]
    else:
        raise AmbiguousArchiveIdError(id_or_path)
