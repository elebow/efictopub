import re

from efictopub import config
from efictopub.fetchers import BaseFetcher
from efictopub.lib import reddit_util
from efictopub.models.reddit import RedditSubmission
from efictopub.models.story import Story


def can_handle_url(url):
    return re.search(r"(?:\w+:\/\/)?(?:\w+)?reddit.com\/u\/\w+.*", url)


class Fetcher(BaseFetcher):
    def __init__(self, url, *, pattern=r""):
        self.reddit = reddit_util.setup_reddit()
        self.author_name = reddit_util.redditor_name_from_url(url)
        self.pattern = pattern

        if not config.get("fetch_comments", bool):
            print(
                "WARNING: fetch_comments is disabled. Chapter bodies sometimes continue in comments. You might be missing chapter content!"
            )

    def fetch_story(self):
        submissions = self.fetch_submissions()
        title = config.get("title")  # reddit story titles must be supplied manually
        author = submissions[0].author_name
        return Story(
            title=title,
            author=author,
            chapters=[subm.as_chapter() for subm in submissions],
        )

    def fetch_submissions(self):
        author = self.reddit.redditor(self.author_name)
        regex = re.compile(self.pattern)
        return [
            RedditSubmission(subm)
            for subm in author.submissions.new()
            if regex.search(subm.title)
        ]
