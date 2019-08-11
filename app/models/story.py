from datetime import datetime
import functools
import urllib.parse

from app.cover_generator import CoverGenerator


class Story:
    ATTRIBUTES = ["title", "author", "summary", "chapters", "date_fetched"]

    def __init__(
        self, *, title=None, author=None, summary=None, chapters, date_fetched=None
    ):
        self.title = title
        self.author = author
        self.summary = summary
        self.chapters = chapters
        if date_fetched is None:
            self.date_fetched = datetime.now().timestamp()
        else:
            self.date_fetched = date_fetched

    @property
    @functools.lru_cache()
    def date_start(self):
        return int(min([chapter.date_published for chapter in self.chapters]))

    @property
    @functools.lru_cache()
    def date_end(self):
        return int(
            max(
                [
                    max(chapter.date_published, chapter.date_updated)
                    for chapter in self.chapters
                ]
            )
        )

    @property
    def filename(self):
        return self.title + " - " + self.author

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
        return {attr: getattr(self, attr) for attr in self.ATTRIBUTES}

    @classmethod
    def from_dict(cls, mapping):
        return cls(**{attr: mapping[attr] for attr in cls.ATTRIBUTES})
