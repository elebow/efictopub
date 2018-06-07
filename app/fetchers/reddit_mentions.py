import praw

from app import fetchers
from app.lib import reddit_util
from app.markdown_parser import MarkdownParser
from app.models import reddit
from app.models.story import Story


class RedditMentions(fetchers.BaseFetcher):
    def __init__(self):
        self.reddit = reddit_util.setup_reddit()

    def fetch_story(self):
        return Story(chapters=self.fetch_chapters())

    def fetch_chapters(self):
        raise "Not yet implemented"

    def submissions_in_list_of_ids(self, id_list):
        return [reddit.Submission(praw.models.Submission(self.reddit, id=id)) for id in id_list]

    def submissions_mentioned_in_reddit_thing(self, thing_or_id_or_url):
        thing = self.parse_thing_or_id_or_url(thing_or_id_or_url)
        links = thing.all_links_in_text()
        return [reddit.Submission(praw.models.Submission(self.reddit, url=link.href)) for link in links]

    def links_mentioned_in_wiki_page(self, url):
        wiki = self.wiki_from_url
        return MarkdownParser(wiki.content_md).links

    def generate_parents(self, start_comm):
        thing = start_comm
        while True:
            yield thing
            if isinstance(thing, praw.models.Submission):
                # praw.models.Submission is the top. Only Comments have parents.
                return
            thing = thing.parent()
