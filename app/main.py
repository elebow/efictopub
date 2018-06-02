#!python3

import yaml

from app.exceptions import UnknownFetcherError
from app.fetcher import Fetcher


class Main:
    def __init__(self, args):
        self.args = args
        self.fetcher = Fetcher()

    def run(self):
        if self.args.fetcher == "reddit_next":
            story = self.fetcher.fetch_from_reddit(self.args.target)
        elif self.args.fetcher == "archive":
            story = self.fetcher.fetch_from_archive(self.args.target)
        else:
            raise UnknownFetcherError(f"Unknown fetcher `{self.args.fetcher}`")

        print(yaml.dump(story))
