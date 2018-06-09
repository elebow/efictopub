import app.archive
from app import fetchers


class Archive(fetchers.BaseFetcher):
    """
    Fetch a story from the archive.
    Note that ID can be partial, as long as it is unique. (TODO)
    """

    def fetch_story(self, id):
        return app.archive.Archive.get(id)

    def fetch_chapters(self):
        pass
