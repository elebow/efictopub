import glob
from pathlib import Path
import yaml

from app import config
from app.exceptions import NoArchivedStoryError, AmbiguousArchiveIdError
from app.models.story import Story
from app.models.chapter import Chapter
from app.models.comment import Comment


"""Saves and retrieves copies of stories on disk."""


def get(id_or_path):
    with open(id_or_path_to_path(id_or_path), "r") as infile:
        return yaml.safe_load(infile)


def store(story):
    path = path_for_story(story)
    with open(path, "w") as outfile:
        return yaml.safe_dump(story, outfile)


def path_for_story(story):
    return f"{config.archive.location}/{story.id}.yml"


def id_or_path_to_path(id_or_path):
    archive_file = Path(id_or_path)
    if archive_file.is_file():
        # id_or_path is already a path. Or the user is very unlucky.
        return id_or_path

    candidates = glob.glob(f"{config.archive.location}/{id_or_path}*")
    num_candidates = len(candidates)
    if num_candidates == 0:
        raise NoArchivedStoryError(id_or_path)
    elif num_candidates == 1:
        return candidates[0]
    else:
        raise AmbiguousArchiveIdError(id_or_path)


def story_representer(dumper, story):
    """Represent a Story object in a way that can be encoded as YAML"""
    return dumper.represent_mapping(u"!story", story.as_dict())


def story_constructor(loader, node):
    """Build a Story object from a representation that can be encoded as YAML"""
    mapping = loader.construct_mapping(node)
    # TODO why is chapters coming back blank from construct_mapping?
    chapters = loader.construct_sequence(node.value[0][1])
    return Story(title=mapping["title"], chapters=chapters)


yaml.SafeDumper.add_representer(Story, story_representer)
yaml.SafeLoader.add_constructor(u'!story', story_constructor)


def chapter_representer(dumper, chapter):
    """Represent a Chapter object in a way that can be encoded as YAML"""
    return dumper.represent_mapping(u"!chapter", chapter.as_dict())


def chapter_constructor(loader, node):
    """Build a Chapter object from a representation that can be encoded as YAML"""
    mapping = loader.construct_mapping(node)
    return Chapter.from_dict(mapping)


yaml.SafeDumper.add_representer(Chapter, chapter_representer)
yaml.SafeLoader.add_constructor(u'!chapter', chapter_constructor)


def comment_representer(dumper, comment):
    """Represent a Comment object in a way that can be encoded as YAML"""
    return dumper.represent_mapping(u"!comment", comment.as_dict())


def comment_constructor(loader, node):
    """Build a Comment object from a representation that can be encoded as YAML"""
    mapping = loader.construct_mapping(node)
    return Comment.from_dict(mapping)


yaml.SafeDumper.add_representer(Comment, comment_representer)
yaml.SafeLoader.add_constructor(u'!comment', comment_constructor)
