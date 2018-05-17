import praw
import re
from collections import namedtuple

from app.markdown_parser import MarkdownParser


class SubmissionCollector:
    Submission = namedtuple("Submission",
                            ["author_name",
                             "comments",
                             "created_utc",
                             "edited",
                             "reddit_id",
                             "permalink",
                             "selftext",
                             "title",
                             "ups"])
    Comment = namedtuple("Comment",
                         ["author_name",
                          "author_flair_text",
                          "body",
                          "created_utc",
                          "edited",
                          "reddit_id",
                          "permalink",
                          "replies",
                          "ups"])

    def __init__(self, *, app, secret, user_agent):
        self.setup_reddit(app, secret, user_agent)

    def all_submissions_by_author_name(self, author_name):
        author = self.reddit.redditor(author_name)
        return [self.extract_subm_attrs(subm) for subm in author.submissions.new(limit=3)]

    def all_submissions_in_list_of_ids(self, id_list):
        return [self.extract_subm_attrs(praw.models.Submission(self.reddit, id=id)) for id in id_list]

    def all_submissions_mentioned_in_reddit_thing(self, thing_or_id_or_url):
        # TODO figure out if it's a subm, comment, or wiki page and call the appropriate method
        subm = True
        comm = False
        wiki = False
        if subm:
            links = self.all_links_mentioned_in_submission(thing_or_id_or_url)
        elif comm:
            links = self.all_links_mentioned_in_comment(thing_or_id_or_url)
        elif wiki:
            links = self.all_links_mentioned_in_wiki_page(thing_or_id_or_url)
        return [self.extract_subm_attrs(praw.models.Submission(self.reddit, url=link.href)) for link in links]

    def all_links_mentioned_in_submission(self, subm_or_id_or_url):
        subm = self.subm_from_id_or_url(subm_or_id_or_url)
        return MarkdownParser(subm.selftext).links

    def all_links_mentioned_in_comment(self, comm_or_id_or_url):
        comm = self.comm_from_id_or_url(comm_or_id_or_url)
        return MarkdownParser(comm.body).links

    def all_submissions_mentioned_in_wiki_page(self, url):
        wiki = self.wiki_from_url
        return MarkdownParser(wiki.content_md).links

    def all_submissions_following_next_links(self, start_subm_id):
        start_subm = praw.models.Submission(self.reddit, id=start_subm_id)
        return [self.extract_subm_attrs(subm) for subm in self.generate_next_submissions(start_subm)]

    def comment_chain_ending_with_comment(self, comment_id):
        # TODO
        pass

    def all_comments_for_submission(self, subm):
        subm.comments.replace_more(limit=None)
        return [self.extract_comm_attrs(comm) for comm in subm.comments]

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

    # Return array of Comment namedtuples that are replies to the given comment
    def replies_for_comment(self, comm):
        return [self.extract_comm_attrs(c) for c in comm.replies]

    def subm_from_id_or_url(self, subm):
        if isinstance(subm, praw.models.Submission):
            # already in the form we want
            return subm
        elif isinstance(subm, str):
            if len(subm) == 6:
                return praw.models.Submission(self.reddit, id=subm)
            else:
                # longer than 6 characters, assume it's a URL
                return praw.models.Submission(self.reddit, url=subm)

    def comm_from_id_or_url(self, comm):
        if isinstance(comm, praw.models.Comment):
            # already in the form we want
            return comm
        elif isinstance(comm, str):
            if len(comm) == 6:
                return praw.models.Comment(self.reddit, id=comm)
            else:
                # longer than 6 characters, assume it's a URL
                return praw.models.Comment(self.reddit, url=comm)

    def wiki_from_url(self, wiki_or_url):
        if isinstance(wiki_or_url, praw.models.WikiPage):
            # already in the form we want
            return wiki_or_url
        elif isinstance(wiki_or_url, str):
            matches = re.findall(r'.*reddit.com/r/(.*?)/wiki/(.*)$', wiki_or_url)[0]
            subreddit = matches[0]
            name = matches[1]
            return praw.models.WikiPage(self.reddit, subreddit, name)

    def extract_comm_attrs(self, comm):
        return self.Comment(author_name=comm.author.name if comm.author else "[n/a]",
                            author_flair_text=comm.author_flair_text,
                            body=comm.body,
                            created_utc=comm.created_utc,
                            edited=comm.edited,
                            reddit_id=comm.id,
                            replies=self.replies_for_comment(comm),
                            permalink=comm.permalink,
                            ups=comm.ups)

    def extract_subm_attrs(self, subm):
        return self.Submission(author_name=subm.author.name,
                               comments=self.all_comments_for_submission(subm),
                               created_utc=subm.created_utc,
                               edited=subm.edited,
                               reddit_id=subm.id,
                               permalink=subm.permalink,
                               selftext=subm.selftext,
                               title=subm.title,
                               ups=subm.ups)

    def setup_reddit(self, app, secret, user_agent):
        self.reddit = praw.Reddit(client_id=app, client_secret=secret, user_agent=user_agent)
