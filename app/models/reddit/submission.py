import functools

from app.models import reddit
from app.models.chapter import Chapter

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
        return [reddit.Comment(comm) for comm in praw_submission.comments]

    def all_links_in_text(self):
        return MarkdownParser(self.selftext).links

    @functools.lru_cache()
    def get_text(self):
        """Extract the text from the submission body and zero or more comments."""
        text = self.selftext

        if not self.comments:
            return text

        comment = self.comments[0]
        while True:
            if len(comment.body) > 2000:
                # Dumb heuristic to differentiate author notes from actual content
                text += comment.body
                comment.body = "[efictopub]: included in chapter text"

            if comment.replies == []:
                break
            comment = comment.replies[0]

        return text

    @functools.lru_cache()
    def as_dict(self):
        attr_names = ["author_name", "created_utc", "edited", "reddit_id", "permalink", "selftext", "title",
                      "ups"]
        attrs = {name: getattr(self, name) for name in attr_names}
        attrs["comments"] = [comment.as_dict() for comment in self.comments]
        return attrs
