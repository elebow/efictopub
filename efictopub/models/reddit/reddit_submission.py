import bs4
import functools

from efictopub import config
from efictopub.models.reddit import RedditComment
from efictopub.models.chapter import Chapter


class RedditSubmission:
    def __init__(self, praw_submission):
        self.author_name = self.format_author_name(praw_submission)
        # The body text sometimes continues in a comment, so fetch all comments at first
        self.all_comments = self.fetch_all_comments(praw_submission)
        self.created_utc = praw_submission.created_utc
        self.edited = praw_submission.edited
        self.reddit_id = praw_submission.id
        self.permalink = praw_submission.permalink
        self.selftext_html = praw_submission.selftext_html
        self.title = praw_submission.title
        self.ups = praw_submission.ups

    def fetch_all_comments(self, praw_submission):
        praw_submission.comments.replace_more(limit=None)
        return [RedditComment(comm).as_comment() for comm in praw_submission.comments]

    @property
    @functools.lru_cache()
    def text(self):
        """Extract the text from the submission body and zero or more comments."""
        text = self.trim_html(self.selftext_html)

        if not self.all_comments:
            return text

        comment = self.all_comments[0]
        while True:
            if len(comment.text) > 2000:
                # Dumb heuristic to differentiate author notes from actual content
                text += "\n\n" + comment.text
                comment.text = "[efictopub]: included in chapter text"

            if comment.replies == []:
                break
            comment = comment.replies[0]

        return text

    @property
    def comments(self):
        if config.get("comments") != "none":
            return self.all_comments
        return []

    def trim_html(self, html):
        dom = bs4.BeautifulSoup(html, "lxml").body

        # strip comments
        for comment in dom.findAll(text=lambda text: isinstance(text, bs4.Comment)):
            comment.extract()

        # Strip the containing <div>
        containing_div = dom.find("div", {"class": "md"})
        if containing_div:
            containing_div.unwrap()

        return dom.encode_contents().decode()

    def format_author_name(self, praw_submission):
        author_flair_text = praw_submission.author_flair_text
        if author_flair_text:
            return f"{praw_submission.author.name} ({author_flair_text})"
        else:
            return praw_submission.author.name

    @functools.lru_cache()
    def as_chapter(self):
        return Chapter(
            comments=self.comments,
            date_published=self.created_utc,
            # self.edited is a timestamp or False.
            # In Python 3, False == 0, but cast it to an int to make sure it serializes correctly.
            date_updated=int(self.edited),
            permalink=self.permalink,
            score=self.ups,
            text=self.text,
            title=self.title,
        )
