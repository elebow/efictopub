import functools

from app import archive
from app import config
from app import fetchers
from app import git
from app.epub_writer import EpubWriter


class Controller:
    def __init__(self, args={}):
        self.args = args
        self.store_args_in_config()

    def run(self):
        config.load(self.args.config_file)

        if git.repo_is_dirty() and self.args.archive and not self.args.clobber:
            print("Git repo has uncommitted changes! Refusing to continue. Do one or more of the following:"
                  f"1. Commit, reset, or otherwise settle the git repo at #{config.archive.location}"
                  "2. Add the --no-archive option to omit writing to the archive."
                  "3. Add the --clobber option to clobber uncommitted changes in the archive.")
            return
        self.archive_story()

        if self.args.write_epub:
            self.output_story()

    @property
    @functools.lru_cache()
    def story(self):
        if self.args.fetcher:
            fetcher = fetchers.fetcher_by_name(self.args.fetcher, self.args.target)
        else:
            fetcher = fetchers.fetcher_for_url(self.args.target)
        return fetcher.fetch_story()

    def output_story(self):
        outfile = self.args.outfile if self.args.outfile else "book.epub"
        EpubWriter(self.story, outfile).write_epub()
        print(f"wrote {outfile}")

    def archive_story(self):
        git.commit_story(self.story, f"Local changes before fetching {self.story.title}")
        archive.store(self.story)
        git.commit_story(self.story, f"Fetch {self.story.title}")
        if git.previous_commit_is_not_efic(self.story):
            print("This story's git history contains commits made outside of this program."
                  "Please review these commits so that your changes are not lost!")

    def store_args_in_config(self):
        config.store_options(self.args)
