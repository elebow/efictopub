from efictopub.cli import opts
from efictopub.efictopub import Efictopub


def run():
    options = opts.get()
    efictopub = Efictopub(options)

    if options["write_archive"] and efictopub.fetcher.__module__ != "archive":
        efictopub.archive_story()

    if options["write_epub"]:
        efictopub.write_epub()
