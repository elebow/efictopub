import praw
import re

from efictopub import config
from efictopub import fetchers
from efictopub.lib import reddit_util
from efictopub.html_parser import HTMLParser
from efictopub.models import reddit
from efictopub.models.story import Story


def can_handle_url(url):
    return re.search(r"(?:\w+:\/\/)?(?:\w+)?reddit.com\/r\/\w+\/wiki\/\w+.*", url)


class Fetcher(fetchers.BaseFetcher):
    def __init__(self, url):
        self.url = url
        self.reddit = reddit_util.setup_reddit()

        if not config.get("fetch_comments", bool):
            print(
                "WARNING: fetch_comments is disabled. Chapter bodies sometimes continue in comments. You might be missing chapter content!"
            )

    def fetch_story(self):
        submissions = self.fetch_submissions()
        title = config.get("title")  # reddit story titles must be supplied manually
        author = submissions[0].author
        return Story(
            title=title,
            author=author,
            chapters=[subm.as_chapter() for subm in submissions],
        )

    def fetch_submissions(self):
        return [
            reddit.Submission(praw.models.Submission(self.reddit, url=link.href))
            for link in self.links_mentioned_in_wiki_page()
        ]

    def links_mentioned_in_wiki_page(self):
        wikipage = reddit_util.parse_id_or_url(self.url, self.reddit)
        links = HTMLParser(wikipage.html).links
        return [link for link in links if "/wiki/" not in link.href]

    def generate_parents(self, start_comm):
        thing = start_comm
        while True:
            yield thing
            if isinstance(thing, praw.models.Submission):
                # praw.models.Submission is the top. Only Comments have parents.
                return
            thing = thing.parent()
