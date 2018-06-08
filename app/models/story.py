import urllib.parse


class Story:
    def __init__(self, *, title=None, chapters):
        self.manual_title = title
        self.chapters = chapters
        self.author_name = chapters[0].author_name  # assume all the chapters have the same author
        self.date_start = chapters[0].created_utc
        self.date_end = chapters[-1].created_utc

        self.title = self.calculate_title()
        self.id = self.calculate_id()

    def calculate_id(self):
        return urllib.parse.quote_plus(str(self.date_start) + self.chapters[0].permalink)

    def calculate_title(self):
        if self.manual_title:
            return self.manual_title

        return self.chapters[0].title
