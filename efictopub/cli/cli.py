from efictopub.cli import opts
from efictopub.efictopub import Efictopub


def run():
    options = opts.get()
    efictopub = Efictopub(options)

    if not efictopub.repo_ready_for_write():
        print(
            "Git repo has uncommitted changes! Refusing to continue. Do one or more of the following:\n"
            f"1. Commit, reset, or otherwise settle the git repo at {efictopub.config.get('archive_location')}\n"
            "2. Add the --no-archive option to omit writing to the archive.\n"
            "3. Add the --clobber option to clobber uncommitted changes in the archive."
        )
        return

    if options["write_archive"] and efictopub.fetcher.__module__ != "archive":
        efictopub.archive_story()

    if options["write_epub"]:
        efictopub.write_epub()
