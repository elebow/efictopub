import praw
import re

from app import config
from app.markdown_parser import MarkdownParser
from app.models.submission import Submission
from app.models.comment import Comment
from app.exceptions import AmbiguousIdError


class RedditFetcher:
    def __init__(self):
        self.setup_reddit(config.reddit.app,
                          config.reddit.secret,
                          config.reddit.user_agent)

    def submissions_by_author(self, *, author_name, pattern=r""):
        author = self.reddit.redditor(author_name)
        regex = re.compile(pattern)
        return [Submission(subm) for subm in author.submissions.new() if regex.search(subm.title)]

    def submissions_in_list_of_ids(self, id_list):
        return [Submission(praw.models.Submission(self.reddit, id=id)) for id in id_list]

    def submissions_following_next_links(self, start_subm_id):
        start_subm = praw.models.Submission(self.reddit, id=start_subm_id)
        return [Submission(subm) for subm in self.generate_next_submissions(start_subm)]

    def comment_chain_ending_with_comment(self, last_comm_id):
        last_comm = praw.models.Comment(self.reddit, id=last_comm_id)
        return [Submission(comm) for comm in self.generate_parents(last_comm)]
        # TODO Pretend that each comment is a new submission, and just return an array of subm namedtuples

    def submissions_mentioned_in_reddit_thing(self, thing_or_id_or_url):
        thing = self.parse_thing_or_id_or_url(thing_or_id_or_url)
        links = thing.all_links_in_text()
        return [Submission(praw.models.Submission(self.reddit, url=link.href)) for link in links]

    def links_mentioned_in_wiki_page(self, url):
        wiki = self.wiki_from_url
        return MarkdownParser(wiki.content_md).links

    # Generate Submission objects by following "next" links, including the specified starting submission
    # Raises exception if there's more than one link that contains the word "next"
    def generate_next_submissions(self, start_subm):
        subm = start_subm
        while True:
            yield subm
            next_links = MarkdownParser(subm.selftext).links_containing_text("next")
            if len(next_links) > 1:
                raise "Ambiguous next submission"  # TODO
            elif len(next_links) == 0:
                return
            subm = praw.models.Submission(self.reddit, url=next_links[0].href)

    def generate_parents(self, start_comm):
        thing = start_comm
        while True:
            yield thing
            if isinstance(thing, praw.models.Submission):
                return
            thing = thing.parent()

    def parse_thing_or_id_or_url(self, thing):
        if isinstance(thing, praw.models.Submission):
            return Submission(thing)
        elif isinstance(thing, praw.models.Comment):
            return Comment(thing)
        elif isinstance(thing, praw.models.WikiPage):
            return None #WikiPage(thing) #TODO
        elif isinstance(thing, str):
            if len(thing) == 6:
                raise AmbiguousIdError
            # longer than 6 characters, assume it's a URL
            return self.parse_url(thing)

    def parse_url(self, url):
        if re.match(r'.*reddit.com/r/[^/]*?/comments/[^/]*?/[^/]*/?$', url):
            return Submission(praw.models.Submission(self.reddit, url=url))

        if re.match(r'.*reddit.com/r/[^/]*?/comments/[^/]*?/[^/]*/[^/]*/?$', url):
            return Comment(praw.models.Comment(self.reddit, url=url))

        return None #TODO
        matches = re.findall(r'.*reddit.com/r/(.*?)/wiki/(.*)$', url)[0]
        if matches:
            subreddit = matches[0]
            name = matches[1]
            return WikiPage(praw.models.WikiPage(self.reddit, subreddit, name))

        return None

    def setup_reddit(self, app, secret, user_agent):
        self.reddit = praw.Reddit(client_id=app, client_secret=secret, user_agent=user_agent)
