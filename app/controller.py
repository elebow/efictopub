import functools
import os

from app import archive
from app import config
from app import fetchers
from app import git
from app.epub_writer import EpubWriter


class Controller:
    def __init__(self, args={}):
        self.args = args

    def run(self):
        config.load(args=self.args, fetcher=self.fetcher)

        if (
            git.repo_is_dirty()
            and config.config["write_archive"].get(bool)
            and not config.config["clobber"].get(bool)
        ):
            print(
                "Git repo has uncommitted changes! Refusing to continue. Do one or more of the following:\n"
                f"1. Commit, reset, or otherwise settle the git repo at {config.config['archive_location']}\n"
                "2. Add the --no-archive option to omit writing to the archive.\n"
                "3. Add the --clobber option to clobber uncommitted changes in the archive."
            )
            return

        if (
            config.config["write_archive"].get(bool)
            and not self.fetcher.__module__ == "archive"
        ):
            self.archive_story()

        if config.config["write_epub"].get(bool):
            self.output_story()

    @property
    @functools.lru_cache()
    def story(self):
        return self.fetcher.fetch_story()

    def output_story(self):
        EpubWriter(self.story, self.output_filename).write_epub()
        print(f"wrote {self.output_filename}")

    @property
    @functools.lru_cache()
    def output_filename(self):
        if self.args.outfile:
            return self.args.outfile
        # TODO move this to EpubWriter
        return os.path.join(config.config["epub_location"].get(), self.story.id)

    def archive_story(self):
        git.commit_story(
            self.story, f"Local changes before fetching {self.story.title}"
        )
        archive.store(self.story)
        git.commit_story(self.story, f"Fetch {self.story.title}")
        if git.previous_commit_is_not_efic(self.story):
            print(
                "This story's git history contains commits made outside of this program."
                "Please review these commits so that your changes are not lost!"
            )

    @property
    @functools.lru_cache()
    def fetcher(self):
        if self.args.fetcher:
            return fetchers.fetcher_by_name(self.args.fetcher, self.args.target)
        else:
            return fetchers.fetcher_for_url(self.args.target)
