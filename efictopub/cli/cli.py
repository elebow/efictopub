from efictopub.cli import opts
from efictopub.efictopub import Efictopub

# See https://confuse.readthedocs.io/en/latest/#search-paths for config file locations


def run():
    options = opts.get()
    efictopub = Efictopub(options)

    if options["write_archive"] and efictopub.fetcher.__module__ != "archive":
        efictopub.archive_story()

    if options["write_epub"]:
        efictopub.write_epub()
