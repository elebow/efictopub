#!python3

import yaml

from app.fetcher import Fetcher


class Main:
    def __init__(self, args):
        self.args = args
        self.fetcher = Fetcher()

    def run(self):
        #TODO use self.args to determine what to do

        r_id = "8kgo40"
        story = self.fetcher.fetch_from_reddit(r_id)
        print(yaml.dump(story))
