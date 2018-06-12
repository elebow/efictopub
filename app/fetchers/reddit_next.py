import praw

from app import fetchers
from app.lib import reddit_util
from app.markdown_parser import MarkdownParser
from app.models import reddit
from app.models.story import Story
from app.exceptions import AmbiguousNextError


class RedditNext(fetchers.BaseFetcher):
    """Fetch Reddit submissions by following "next" links in the body"""

    def __init__(self, start_thing_or_id_or_url):
        self.reddit = reddit_util.setup_reddit()
        self.start_thing_or_id_or_url = start_thing_or_id_or_url

    def fetch_story(self):
        return Story(chapters=self.fetch_chapters())

    def fetch_chapters(self):
        start_subm = reddit_util.parse_thing_or_id_or_url(self.start_thing_or_id_or_url, self.reddit)
        return [subm.as_chapter() for subm in self.generate_next_submissions(start_subm)]

    # Generate reddit.Submission objects by following "next" links, including the specified starting
    # submission. Raises exception if there's more than one link that contains the word "next"
    def generate_next_submissions(self, start_subm):
        subm = start_subm
        while True:
            yield subm
            next_links = MarkdownParser(subm.selftext).links_containing_text("next")
            if len(next_links) > 1:
                raise AmbiguousNextError
            elif len(next_links) == 0:
                return
            subm = reddit.Submission(praw.models.Submission(self.reddit, url=next_links[0].href))
