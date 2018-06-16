import os
import yaml

from app import config
from app.models.story import Story
from app.models.chapter import Chapter
from app.models.comment import Comment


class Archive:
    """Saves and retrieves copies of stories on disk."""

    @staticmethod
    def get(id):
        # TODO accept partial ids, as long as they map to a unique file
        # TODO if id contains a slash, assume it is a path rather than an id.
        #    No, use a more reliable heuristic than presence of a slash
        with open(Archive.path(id), "r") as infile:
            return yaml.safe_load(infile)

    @staticmethod
    def store(story):
        with open(Archive.path(story.id), "w") as outfile:
            return yaml.safe_dump(story, outfile)

    @staticmethod
    def path(id):
        return f"{config.archive.location}/{id}.yml"


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
