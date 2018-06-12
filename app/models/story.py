import urllib.parse


class Story:
    def __init__(self, *, title=None, chapters):
        self.manual_title = title
        self.chapters = chapters
        self.author_name = chapters[0].author  # assume all the chapters have the same author
        self.date_start = min([chapter.date_published for chapter in chapters])
        self.date_end = max([chapter.date_updated for chapter in chapters])  # TODO maybe not edited

        self.title = self.calculate_title()
        self.id = self.calculate_id()

    def calculate_id(self):
        return urllib.parse.quote_plus(str(self.date_start) + self.chapters[0].permalink)

    def calculate_title(self):
        if self.manual_title:
            return self.manual_title

        return self.chapters[0].title

    def as_dict(self):
        return {
            "title": self.title,
            "chapters": self.chapters
        }

    @classmethod
    def from_dict(cls, mapping):
        return cls(title=mapping["title"], chapters=mapping["chapters"])
