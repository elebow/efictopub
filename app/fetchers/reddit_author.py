import re

from app import fetchers
from app.lib import reddit_util
from app.models.reddit import RedditSubmission
from app.models.story import Story


def can_handle_url(url):
    return re.search(r"(?:\w+:\/\/)?(?:\w+)?reddit.com\/u\/\w+.*", url)


class Fetcher(fetchers.BaseFetcher):
    def __init__(self, url, *, pattern=r""):
        self.reddit = reddit_util.setup_reddit()
        self.author_name = reddit_util.redditor_name_from_url(url)
        self.pattern = pattern

    def fetch_story(self):
        return Story(chapters=self.fetch_chapters())

    def fetch_chapters(self):
        return [subm.as_chapter() for subm in self.fetch_submissions()]

    def fetch_submissions(self):
        author = self.reddit.redditor(self.author_name)
        regex = re.compile(self.pattern)
        return [RedditSubmission(subm) for subm in author.submissions.new() if regex.search(subm.title)]
