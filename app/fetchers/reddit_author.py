import re

from app.lib import reddit_util
from app.models import reddit


class RedditAuthor:
    def __init__(self):
        self.reddit = reddit_util.setup_reddit()

    def fetch_chapters(self, *, author_name, pattern=r""):
        author = self.reddit.redditor(author_name)
        regex = re.compile(pattern)
        return [reddit.Submission(subm) for subm in author.submissions.new() if regex.search(subm.title)]
