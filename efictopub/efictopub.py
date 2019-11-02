import confuse

from efictopub import config
from efictopub import archive
from efictopub import fetchers
from efictopub import git
from efictopub.epub_writer import EpubWriter


class Efictopub:
    def __init__(self, opts={}):
        confuse_opts = confuse.Configuration("efictopub", __name__)
        confuse_opts.set_args(opts, dots=True)
        self.opts = confuse_opts.flatten()

        self.fetcher = self.get_fetcher()

        config.load(opts=self.opts, fetcher=self.fetcher)

        # re-merge the CLI opts, because they might have been overriden by
        # fetcher_overrides in config.load
        self.opts.update(opts)

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
        if "fetcher" in self.opts and self.opts["fetcher"] is not None:
            return fetchers.fetcher_by_name(self.opts["fetcher"], self.opts["target"])
        else:
            return fetchers.fetcher_for_url(self.opts["target"])

    def repo_ready_for_write(self):
        return (
            not git.repo_is_dirty()
            or not config.get("write_archive")
            or config.get("clobber")
        )
