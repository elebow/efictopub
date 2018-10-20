import functools

import app.archive
from app import fetchers


def can_handle_url(url):
    return False


class Archive(fetchers.BaseFetcher):
    """
    Fetch a story from the archive.
    Note that ID can be partial, as long as it is unique.
    """

    def __init__(self, id_or_path):
        self.id_or_path = id_or_path

    @functools.lru_cache()
    def fetch_story(self):
        return app.archive.get(self.id_or_path)

    @functools.lru_cache()
    def fetch_chapters(self):
        return self.fetch_story().chapters


FETCHER_CLASS = Archive
