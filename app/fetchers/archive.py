import app.archive
from app import fetchers


class Archive(fetchers.BaseFetcher):
    """
    Fetch a story from the archive.
    Note that ID can be partial, as long as it is unique.
    """

    def __init__(self, id):
        self.id = id

    def fetch_story(self):
        return app.archive.get(self.id)

    def fetch_chapters(self):
        pass
