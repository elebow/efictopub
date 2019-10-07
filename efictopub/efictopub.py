import functools

from efictopub import config
from efictopub import archive
from efictopub import fetchers
from efictopub import git
from efictopub.epub_writer import EpubWriter


class Efictopub:
    def __init__(self, args={}):
        self.args = args
        self.fetcher = self.get_fetcher()

        config.load(args=self.args, fetcher=self.fetcher)

        if not self.check_repo_ready_for_write():
            # TODO move this to cli.py also?
            return

        self.story = self.fetch_story()

    def fetch_story(self):
        return self.fetcher.fetch_story()

    def write_epub(self):
        EpubWriter(self.story).write_epub()

    def archive_story(self):
        archive.store(self.story)
        if git.previous_commit_is_not_efic(self.story):
            print(
                "This story's git history contains commits made outside of this program."
                "Please review these commits so that your changes are not lost!"
            )

    def get_fetcher(self):
        if "fetcher" in self.args and self.args["fetcher"] is not None:
            return fetchers.fetcher_by_name(self.args["fetcher"], self.args["target"])
        else:
            return fetchers.fetcher_for_url(self.args["target"])

    def check_repo_ready_for_write(self):
        if (
            git.repo_is_dirty()
            and config.get("write_archive", bool)
            and not config.get("clobber", bool)
        ):
            print(
                "Git repo has uncommitted changes! Refusing to continue. Do one or more of the following:\n"
                f"1. Commit, reset, or otherwise settle the git repo at {config.get('archive_location')}\n"
                "2. Add the --no-archive option to omit writing to the archive.\n"
                "3. Add the --clobber option to clobber uncommitted changes in the archive."
            )
            return False
        return True
