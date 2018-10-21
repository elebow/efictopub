#!python3

import argparse

from app import config
from app import fetchers
from app.controller import Controller


parser = argparse.ArgumentParser(prog="efictopub",
                                 description="Fetch stories from various sources and optionally generate an "
                                             "EPUB file.")

parser.add_argument("target", type=str,
                    help="target story or document containing list of stories (URL, reddit ID, etc). "
                         "Automatic fetcher selection is supported only for URLs.")

parser.add_argument("--fetcher", "-F", type=str, dest="fetcher", action="store",
                    help=f"fetcher to use ({', '.join(fetchers.fetcher_names())})")

parser.add_argument("--config", "-c", dest="config_file", action="store", default=config.default_config_file,
                    help=f"specify config file (default: {config.default_config_file})")
parser.add_argument("--outfile", "-o", dest="outfile", action="store",
                    help=f"specify output file, for actions that support an output file (default varies per \
                            action)")

parser.add_argument("--no-archive", dest="archive", action="store_false", default=True,
                    help="do not write the story to the archive")
parser.add_argument("--no-comments", dest="comments", action="store_false", default=True,
                    help="do not store or write comments, for fetchers that support comments")
parser.add_argument("--no-write-epub", dest="write_epub", action="store_false", default=True,
                    help="do not write an EPUB file")

args = parser.parse_args()

Controller(args).run()
