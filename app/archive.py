import os
import yaml

from app.models.story import Story


class Archive:
    """Saves and retrieves copies of stories on disk."""

    @staticmethod
    def get(id):
        # TODO accept partial ids, as long as they map to a unique file
        # TODO if id contains a slash, assume it is a path rather than an id. No, use a more reliable heuristic than presence of a slash
        with open(Archive.path(id), "r") as infile:
            return yaml.safe_load(infile)

    @staticmethod
    def store(story):
        with open(Archive.path(story.id), "w") as outfile:
            return yaml.safe_dump(story, outfile)

    @staticmethod
    def path(id):
        return f"{os.environ.get('HOME')}/.efictopub/cache/{id}.yml"  # TODO make configurable


def story_representer(dumper, story):
    """Represent a Story object in a way that can be encoded as YAML"""
    mapping = {
        "title": story.title,
        "chapters": [chapter.as_dict() for chapter in story.chapters]
    }
    return dumper.represent_mapping(u"!story", mapping)


def story_constructor(loader, node):
    """Build a Story object from a representation that can be encoded as YAML"""
    mapping = loader.construct_mapping(node)
    # TODO why is chapters coming back blank from construct_mapping?
    chapters = loader.construct_sequence(node.value[0][1])
    return Story(title=mapping["title"], chapters=chapters)


yaml.SafeDumper.add_representer(Story, story_representer)
yaml.SafeLoader.add_constructor(u'!story', story_constructor)
