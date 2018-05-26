# Module to store config values read from the file

from collections import namedtuple
import os


Reddit = namedtuple("Reddit", ["app", "secret", "user_agent"])
Cache = namedtuple("Cache", ["location"])


def load():
    import configparser
    cfg = configparser.ConfigParser()
    cfg.read("config.ini")  # TODO dotenv?

    global reddit, cache
    reddit = Reddit(app=cfg.get("REDDIT", "app"),
                    secret=cfg.get("REDDIT", "secret"),
                    user_agent=cfg.get("REDDIT", "user_agent"))
    cache = Cache(location=cfg.get("CACHE",
                                   "location",
                                   fallback="%s/.reddit/series-to-epub/cache/" % os.environ.get("HOME")))


load()
