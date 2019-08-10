from datetime import datetime
import functools
import urllib.parse

from app.cover_generator import CoverGenerator


class Story:
    def __init__(self, *, title=None, author=None, summary=None, chapters):
        self.title = title
        self.author = author
        self.summary = summary
        self.chapters = chapters
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
    def cover_svg(self):
        return CoverGenerator(self).generate_cover_svg()

    def as_dict(self):
        return {
            "title": self.title,
            "author": self.author,
            "summary": self.summary,
            "chapters": self.chapters,
        }

    @classmethod
    def from_dict(cls, mapping):
        return cls(
            title=mapping["title"],
            author=mapping["author"],
            summary=mapping["summary"],
            chapters=mapping["chapters"],
        )
