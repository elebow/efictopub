#!python3

import functools
import inspect
import yaml

from app import archive
from app import config
from app.exceptions import UnknownFetcherError
from app import fetchers
from app.epub_writer import EpubWriter


class Main:
    def __init__(self, args={}):
        self.args = args

    def run(self):
        config.load(self.args.config_file)

        story = self.get_story()
        archive.store(story)
        self.output(story)

    def get_story(self):
        if self.args.fetcher in Main._fetcher_names():
            # TODO also pass optional args
            fetcher = Main._fetchers()[self.args.fetcher](self.args.target)
            return fetcher.fetch_story()
        else:
            raise UnknownFetcherError(f"Unknown fetcher `{self.args.fetcher}`")

    def output(self, story):
        if self.args.action == "write_epub":
            EpubWriter(story, "outfile.epub").write_epub()
            print("wrote epub")

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
