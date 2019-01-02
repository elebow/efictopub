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

        self.archive_story()

        if self.args.write_epub:
            self.output(self.story)

    def get_story(self):
        if self.args.fetcher:
            fetcher = fetchers.fetcher_by_name(self.args.fetcher, self.args.target)
        else:
            fetcher = fetchers.fetcher_for_url(self.args.target)
        return fetcher.fetch_story()

    def output(self, story):
        outfile = self.args.outfile if self.args.outfile else "book.epub"
        EpubWriter(story, outfile).write_epub()
        print(f"wrote {outfile}")

    def archive_story(self):
        git.commit_story(self.story, f"Local changes before fetching {self.story.title}")
        archive.store(self.story)
        git.commit_story(self.story, f"Fetch {self.story.title}")

    def store_args_in_config(self):
        config.store_options(self.args)

    @property
    def story(self):
        #TODO just put the contents of get_story() here
        return self.get_story()
