import urllib.parse


class Story:
    def __init__(self, *, title, chapters):
        self.title = title
        self.chapters = chapters
        self.author = chapters[0].author  # assume all the chapters have the same author
        self.date_start = chapters[0].created_utc
        self.date_end = chapters[-1].created_utc

        self.id = self.calculate_id()

    def calculate_id(self):
        return urllib.parse.quote_plus(self.date_start + self.chapters[0].permalink)
