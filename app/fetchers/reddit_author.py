import re

from app import fetchers
from app.lib import reddit_util
from app.models import reddit
from app.models.story import Story


class RedditAuthor(fetchers.BaseFetcher):
    def __init__(self, *, author_name, pattern=r""):
        self.reddit = reddit_util.setup_reddit()
        self.author_name = author_name
        self.pattern = pattern

    def fetch_story(self):
        return Story(chapters=self.fetch_chapters())

    def fetch_chapters(self):
        author = self.reddit.redditor(self.author_name)
        regex = re.compile(self.pattern)
        return [reddit.Submission(subm) for subm in author.submissions.new() if regex.search(subm.title)]
