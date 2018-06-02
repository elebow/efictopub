#!python3

import yaml

from app.exceptions import UnknownModeError
from app.fetcher import Fetcher


class Main:
    def __init__(self, args):
        self.args = args
        self.fetcher = Fetcher()

    def run(self):
        if self.args.mode == "reddit_next":
            story = self.fetcher.fetch_from_reddit(self.args.target)
        elif self.args.mode == "archive":
            story = self.fetcher.fetch_from_archive(self.args.target)
        else:
            raise UnknownModeError(f"Unknown mode `{self.args.mode}`")

        print(yaml.dump(story))
