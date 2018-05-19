#!/usr/bin/python3

import json
import sys

from reddit_fetcher import RedditFetcher


class Main:
    def __init__(self):
        self.load_config()
        self.reddit_fetcher = RedditFetcher(app=self.app,
                                            secret=self.secret,
                                            user_agent=self.user_agent)

    def author_submissions_to_json(self, author_name):
        submissions = self.reddit_fetcher.all_submissions_by_author_name(author_name)
        print(json.dumps(submissions))

    def load_config(self):
        import configparser
        cfg = configparser.ConfigParser()
        cfg.read(sys.argv[1])

        self.app = cfg.get('DEFAULT', 'app')
        self.secret = cfg.get('DEFAULT', 'secret')
        self.user_agent = cfg.get("DEFAULT", "user_agent")


if __name__ == "__main__":
    Main().author_submissions_to_json(sys.argv[2])
