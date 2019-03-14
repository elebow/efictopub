# Module to store config values read from the file

from collections import namedtuple
import os


Reddit = namedtuple("Reddit", ["app", "secret", "user_agent"])
Archive = namedtuple("Archive", ["location"])
Output = namedtuple("Output", ["dir"])
Options = namedtuple("Options", ["fetch_comments", "write_archive", "write_epub"])


default_config_file = f"{os.environ.get('HOME')}/.efictopub/config.ini"


def load(filename):
    import configparser
    cfg = configparser.ConfigParser()
    cfg.read(filename)

    global reddit, archive, output
    reddit = Reddit(app=cfg.get("REDDIT", "app"),
                    secret=cfg.get("REDDIT", "secret"),
                    user_agent=cfg.get("REDDIT", "user_agent"))
    archive = Archive(location=cfg.get("ARCHIVE",
                                       "location",
                                       fallback="%s/.efictopub/archive" % os.environ.get("HOME")))
    output = Output(dir=cfg.get("OUTPUT",
                                "dir",
                                fallback=os.environ.get("HOME")))


def store_options(args):
    global options
    options = Options(fetch_comments=args.comments,
                      write_archive=args.archive,
                      write_epub=args.write_epub)


load(default_config_file)   # always attempt to load the default, in case we load this module by itself
