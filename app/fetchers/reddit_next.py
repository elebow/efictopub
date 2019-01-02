import praw
import re

from app import fetchers
from app.lib import reddit_util
from app.markdown_parser import MarkdownParser
from app.models import reddit
from app.models.story import Story
from app.exceptions import AmbiguousNextError


def can_handle_url(url):
    return re.search(r"(?:\w+:\/\/)?(?:\w+)?reddit.com\/r\/\w+\/comments\/\w+.*", url)


class RedditNext(fetchers.BaseFetcher):
    """Fetch Reddit submissions by following "next" links in the body"""

    def __init__(self, start_id_or_url):
        self.reddit = reddit_util.setup_reddit()
        self.start_id_or_url = start_id_or_url

    def fetch_story(self):
        return Story(chapters=self.fetch_chapters())

    def fetch_chapters(self):
        start_subm = reddit_util.parse_id_or_url(self.start_id_or_url, self.reddit)
        return [subm.as_chapter() for subm in self.generate_next_submissions(start_subm)]

    # Generate reddit.Submission objects by following "next" links, including the specified starting
    # submission. Raises exception if there's more than one link that contains the word "next"
    def generate_next_submissions(self, start_subm):
        subm = start_subm
        while True:
            yield subm
            next_links = MarkdownParser(subm.selftext).links_containing_text("next")
            next_urls = list(set([link.href for link in next_links]))
            if len(next_urls) > 1:
                raise AmbiguousNextError
            elif len(next_urls) == 0:
                return
            subm = reddit.Submission(praw.models.Submission(self.reddit, url=next_urls[0]))


FETCHER_CLASS = RedditNext
