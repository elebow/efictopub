import re

from efictopub import config
from efictopub.fetchers import BaseFetcher
from efictopub.lib import reddit_util
from efictopub.models.reddit import RedditSubmission
from efictopub.models.story import Story


def can_handle_url(url):
    return re.search(r"^(?:\w+:\/\/)?(?:\w+\.)?reddit.com\/u\/\w+.*", url)


class Fetcher(BaseFetcher):
    def __init__(self, url):
        self.reddit = reddit_util.setup_reddit()
        self.author_name = reddit_util.redditor_name_from_url(url)

        title_pattern_opt = config.get_fetcher_opt("title_pattern")
        if title_pattern_opt:
            self.title_pattern = re.compile(title_pattern_opt)
        else:
            self.title_pattern = None

        if not config.get("fetch_comments"):
            print(
                "WARNING: fetch_comments is disabled. Chapter bodies sometimes continue in comments. You might be missing chapter content!"
            )

    def fetch_story(self):
        submissions = self.fetch_submissions()
        title = config.get_fetcher_opt("title", required=True)
        author = submissions[0].author_name
        return Story(
            title=title,
            author=author,
            chapters=[subm.as_chapter() for subm in submissions],
        )

    def fetch_submissions(self):
        author = self.reddit.redditor(self.author_name)
        return [
            RedditSubmission(subm)
            for subm in author.submissions.new()
            if self.title_pattern is None or self.title_pattern.search(subm.title)
        ]
