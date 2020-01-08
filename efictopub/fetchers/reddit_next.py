import functools
import re

from efictopub import config
from efictopub.fetchers import BaseFetcher
from efictopub.lib import reddit_util
from efictopub.html_parser import HTMLParser
from efictopub.models.story import Story
from efictopub.exceptions import AmbiguousNextError


def can_handle_url(url):
    return re.search(
        r"^(?:\w+:\/\/)?(?:\w+\.)?reddit.com\/r\/\w+\/comments\/\w+.*", url
    )


class Fetcher(BaseFetcher):
    """Fetch Reddit submissions by following "next" links in the body"""

    def __init__(self, start_id_or_url):
        self.start_id_or_url = start_id_or_url

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
        start_subm = reddit_util.parse_id_or_url(self.start_id_or_url, self.praw_reddit)
        return list(self.generate_next_submissions(start_subm))

    def generate_next_submissions(self, start_subm):
        """
        Generate reddit.Submission objects by following "next" links, including the specified starting
        submission. Raises exception if there's more than one link that contains the word "next"
        """
        subm = start_subm
        while True:
            yield subm
            next_links = HTMLParser(subm.selftext_html).links_containing_text("next")
            next_urls = list(set([link.href for link in next_links]))
            if len(next_urls) > 1:
                raise AmbiguousNextError
            elif len(next_urls) == 0:
                return
            subm = reddit_util.parse_url(next_urls[0], self.praw_reddit)

    @property
    @functools.lru_cache()
    def praw_reddit(self):
        return reddit_util.setup_reddit()
