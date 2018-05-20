class Book:
    def __init__(self, *, title, chapters):
        self.title = title
        self.chapters = chapters
        self.author = chapters[0].author  # assume all the chapters have the same author
