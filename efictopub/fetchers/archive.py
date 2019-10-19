import functools
import pathlib

import efictopub.archive
from efictopub.fetchers import BaseFetcher


def can_handle_url(url):
    path = pathlib.Path(url)
    return path.exists() and path.is_file()


class Fetcher(BaseFetcher):
    """
    Fetch a story from the archive.
    Note that ID can be partial, as long as it is unique. TODO
    """

    def __init__(self, id_or_path):
        self.id_or_path = id_or_path

    @functools.lru_cache()
    def fetch_story(self):
        return efictopub.archive.get(self.id_or_path)

    @functools.lru_cache()
    def fetch_chapters(self):
        return self.fetch_story().chapters
