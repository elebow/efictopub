from datetime import datetime
import functools
import urllib.parse

from app.cover_generator import CoverGenerator


class Story:
    def __init__(self, *, title=None, chapters):
        self.manual_title = title
        self.chapters = chapters
        self.author_name = chapters[
            0
        ].author  # assume all the chapters have the same author
        self.date_fetched = datetime.now().timestamp()

    @property
    @functools.lru_cache()
    def date_start(self):
        return min([chapter.date_published for chapter in self.chapters])

    @property
    @functools.lru_cache()
    def date_end(self):
        return max(
            [
                max(chapter.date_published, chapter.date_updated)
                for chapter in self.chapters
            ]
        )

    @property
    @functools.lru_cache()
    def id(self):
        return urllib.parse.quote_plus(
            str(self.date_start) + self.chapters[0].permalink
        )

    @property
    @functools.lru_cache()
    def title(self):
        if self.manual_title:
            return self.manual_title

        return self.chapters[0].story_title

    def as_dict(self):
        return {"title": self.title, "chapters": self.chapters}

    @property
    @functools.lru_cache()
    def cover_svg(self):
        return CoverGenerator(self).generate_cover_svg()

    @classmethod
    def from_dict(cls, mapping):
        return cls(title=mapping["title"], chapters=mapping["chapters"])
