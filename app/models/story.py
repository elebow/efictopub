import urllib.parse


class Story:
    def __init__(self, *, title=None, chapters):
        self.manual_title = title
        self.chapters = chapters
        self.author_name = chapters[0].author  # assume all the chapters have the same author
        self.date_start = self.calculate_date_start()
        self.date_end = self.calculate_date_end()

        self.title = self.calculate_title()
        self.id = self.calculate_id()

    def calculate_date_start(self):
        return min([chapter.date_published for chapter in self.chapters])

    def calculate_date_end(self):
        return max([max(chapter.date_published, chapter.date_updated) for chapter in self.chapters])

    def calculate_id(self):
        return urllib.parse.quote_plus(str(self.date_start) + self.chapters[0].permalink)

    def calculate_title(self):
        if self.manual_title:
            return self.manual_title

        return "[auto title] " + self.chapters[0].title

    def as_dict(self):
        return {
            "title": self.title,
            "chapters": self.chapters
        }

    @classmethod
    def from_dict(cls, mapping):
        return cls(title=mapping["title"], chapters=mapping["chapters"])
