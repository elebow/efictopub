import praw

from collections import namedtuple

from app.markdown_parser import MarkdownParser


class SubmissionCollector:
    Submission = namedtuple("Submission",
                            ["author_name",
                             "comments",
                             "created_utc",
                             "edited",
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
                          "permalink",
                          "replies",
                          "ups"])

    def __init__(self, *, app, secret, user_agent):
        self.setup_reddit(app, secret, user_agent)

    def all_submissions_by_author_name(self, author_name):
        author = self.reddit.redditor(author_name)
        return [self.extract_subm_attrs(subm) for subm in author.submissions.new(limit=3)]

    def all_submissions_in_list_of_ids(self, id_list):
        # TODO
        pass

    def all_submissions_mentioned_in_reddit_thing(self, thing_id):
        # TODO
        pass

    def all_submissions_mentioned_in_reddit_wiki_page(self, page):
        # TODO
        pass

    def all_submissions_following_next_links(self, start_subm):
        return [self.extract_subm_attrs(subm) for subm in self.generate_next_submissions(start_subm)]

    def comment_chain_ending_with_comment(self, comment_id):
        # TODO
        pass

    def all_comments_for_submission(self, subm):
        subm.comments.replace_more(limit=None)
        return [self.extract_comm_attrs(comm) for comm in subm.comments]

    # Generate Submission namedtuples by following "next" links, including the specified starting submission
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

    def extract_comm_attrs(self, comm):
        return self.Comment(author_name=comm.author.name if comm.author else "[n/a]",
                            author_flair_text=comm.author_flair_text,
                            body=comm.body,
                            created_utc=comm.created_utc,
                            edited=comm.edited,
                            replies=self.replies_for_comment(comm),
                            permalink=comm.permalink,
                            ups=comm.ups)

    def extract_subm_attrs(self, subm):
        return self.Submission(author_name=subm.author.name,
                               comments=self.all_comments_for_submission(subm),
                               created_utc=subm.created_utc,
                               edited=subm.edited,
                               permalink=subm.permalink,
                               selftext=subm.selftext,
                               title=subm.title,
                               ups=subm.ups)

    def setup_reddit(self, app, secret, user_agent):
        self.reddit = praw.Reddit(client_id=app, client_secret=secret, user_agent=user_agent)
