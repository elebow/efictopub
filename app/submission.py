from app.comment import Comment
from app.markdown_parser import MarkdownParser


class Submission:
    def __init__(self, praw_submission):
        self.author_name = praw_submission.author.name
        self.comments = self.fetch_all_comments(praw_submission)
        self.created_utc = praw_submission.created_utc
        self.edited = praw_submission.edited
        self.reddit_id = praw_submission.id
        self.permalink = praw_submission.permalink
        self.selftext = praw_submission.selftext
        self.title = praw_submission.title
        self.ups = praw_submission.ups

    def fetch_all_comments(self, praw_submission):
        praw_submission.comments.replace_more(limit=None)
        return [Comment(comm) for comm in praw_submission.comments]

    def all_links_in_text(self):
        return MarkdownParser(self.selftext).links
