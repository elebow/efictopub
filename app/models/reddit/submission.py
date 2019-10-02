import functools

from app import config
from app.models import reddit
from app.models.chapter import Chapter


class Submission:
    def __init__(self, praw_submission):
        self.author_name = praw_submission.author.name
        if config.options.fetch_comments:
            self.comments = self.fetch_all_comments(praw_submission)
        else:
            self.comments = []
        self.created_utc = praw_submission.created_utc
        self.edited = praw_submission.edited
        self.reddit_id = praw_submission.id
        self.permalink = praw_submission.permalink
        self.selftext_html = praw_submission.selftext_html
        self.title = praw_submission.title
        self.ups = praw_submission.ups

    def fetch_all_comments(self, praw_submission):
        praw_submission.comments.replace_more(limit=None)
        return [reddit.Comment(comm).as_comment() for comm in praw_submission.comments]

    @property
    @functools.lru_cache()
    def text(self):
        """Extract the text from the submission body and zero or more comments."""
        text = self.selftext_html

        if not self.comments:
            return text

        comment = self.comments[0]
        while True:
            if len(comment.text) > 2000:
                # Dumb heuristic to differentiate author notes from actual content
                text += "\n\n" + comment.text
                comment.text = "[efictopub]: included in chapter text"

            if comment.replies == []:
                break
            comment = comment.replies[0]

        return text

    @functools.lru_cache()
    def as_chapter(self):
        return Chapter(author=self.author_name,
                       comments=self.comments,
                       date_published=self.created_utc,
                       date_updated=self.edited,  # TODO self.edited is a timestamp or False
                       permalink=self.permalink,
                       score=self.ups,
                       story_title=f"[auto title] {self.title}",
                       text=self.text,
                       title=self.title)
