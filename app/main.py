#!python3

import functools
import inspect
import yaml

from app.archive import Archive
from app.exceptions import UnknownFetcherError
from app.models.story import Story
from app import fetchers


class Main:
    def __init__(self, args={}):
        self.args = args

    def run(self):
        story = self.get_story()
        Archive.store(story)
        print(yaml.dump(story))

    def get_story(self):
        if self.args.fetcher == "archive":
            """
            Fetch a story from the archive.
            Note that ID can be partial, as long as it is unique.
            """
            return Archive.get(self.args.target)
        elif self.args.fetcher in Main._fetcher_names():
            chapters = self.get_chapters()
            return Story(chapters=chapters)
        else:
            raise UnknownFetcherError(f"Unknown fetcher `{self.args.fetcher}`")

    def get_chapters(self):
        return Main._fetchers()[self.args.fetcher].fetch_chapters(self.args.target)

    @staticmethod
    @functools.lru_cache()
    def _fetcher_names():
        return Main._fetchers().keys()

    @staticmethod
    @functools.lru_cache()
    def _fetchers():
        return dict([fetcher
                    for fetcher
                    in inspect.getmembers(fetchers, inspect.isclass)
                    if fetcher[1] != fetchers.BaseFetcher])
