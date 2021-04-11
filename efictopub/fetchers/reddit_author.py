import re
import functools

from efictopub import config
from efictopub.fetchers import BaseFetcher
from efictopub.lib import reddit_util
from efictopub.models.reddit import RedditSubmission
from efictopub.models.story import Story


def can_handle_url(url):
    return re.search(r"^(?:\w+:\/\/)?(?:\w+\.)?reddit.com\/u\/\w+.*", url)


class Fetcher(BaseFetcher):
    def __init__(self, url):
        self.author_name = reddit_util.redditor_name_from_url(url)

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
        praw_author = self.praw_reddit.redditor(self.author_name)
        submissions = [
            RedditSubmission(subm)
            for subm in praw_author.submissions.new(limit=1000)
            if self.title_pattern is None or self.title_pattern.search(subm.title)
        ]
        return list(reversed(submissions))

    @property
    @functools.lru_cache()
    def praw_reddit(self):
        return reddit_util.setup_reddit()

    @property
    @functools.lru_cache()
    def title_pattern(self):
        title_pattern_opt = config.get_fetcher_opt("title_pattern")
        if title_pattern_opt:
            return re.compile(title_pattern_opt)
        else:
            return None
