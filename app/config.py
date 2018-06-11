# Module to store config values read from the file

from collections import namedtuple
import os


Reddit = namedtuple("Reddit", ["app", "secret", "user_agent"])
Archive = namedtuple("Archive", ["location"])


def load(filename):
    import configparser
    cfg = configparser.ConfigParser()
    cfg.read(filename)

    global reddit, archive
    reddit = Reddit(app=cfg.get("REDDIT", "app"),
                    secret=cfg.get("REDDIT", "secret"),
                    user_agent=cfg.get("REDDIT", "user_agent"))
    archive = Archive(location=cfg.get("ARCHIVE",
                                       "location",
                                       fallback="%s/.efictopub/archive/" % os.environ.get("HOME")))


load("config.ini")  # TODO filename from dotenv?
