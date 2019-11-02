import confuse
import functools

from efictopub import config
from efictopub import archive
from efictopub import fetchers
from efictopub import git
from efictopub.epub_writer import EpubWriter


class Efictopub:
    def __init__(self, opts={}):
        # we have to find the fetcher first because it determines the fetcher_overrides applied in config
        self.fetcher = self.get_fetcher(opts)

        confuse_opts = confuse.Configuration("efictopub", __name__)
        fetcher_overrides = confuse_opts["overrides"].get().get(self.fetcher.__module__)
        if fetcher_overrides:
            # add a second, higher-priority source to the Confuse object
            confuse_opts.set(fetcher_overrides)
        # set_args takes the highest priority
        confuse_opts.set_args(opts, dots=True)
        self.opts = confuse_opts.flatten()

        config.load(opts=self.opts, fetcher=self.fetcher)

    @property
    @functools.lru_cache()
    def story(self):
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

    def get_fetcher(self, opts):
        if "fetcher" in opts and opts["fetcher"] is not None:
            return fetchers.fetcher_by_name(opts["fetcher"], opts["target"])
        else:
            return fetchers.fetcher_for_url(opts["target"])

    def repo_ready_for_write(self):
        return (
            not git.repo_is_dirty()
            or not config.get("write_archive")
            or config.get("clobber")
        )
