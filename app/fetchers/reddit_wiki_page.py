import praw
import re

from app import config
from app import fetchers
from app.lib import reddit_util
from app.html_parser import HTMLParser
from app.models import reddit
from app.models.story import Story


def can_handle_url(url):
    return re.search(r"(?:\w+:\/\/)?(?:\w+)?reddit.com\/r\/\w+\/wiki\/\w+.*", url)


class Fetcher(fetchers.BaseFetcher):
    def __init__(self, url):
        self.url = url
        self.reddit = reddit_util.setup_reddit()

    def fetch_story(self):
        chapters = self.fetch_chapters()
        # It's too hard to infer the story title from a single chapter on reddit
        title = config.get("title")
        author = chapters[0].author
        return Story(title=title, author=author, chapters=chapters)

    def fetch_chapters(self):
        subms = [
            reddit.Submission(praw.models.Submission(self.reddit, url=link.href))
            for link in self.links_mentioned_in_wiki_page()
        ]
        return [subm.as_chapter() for subm in subms]

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
