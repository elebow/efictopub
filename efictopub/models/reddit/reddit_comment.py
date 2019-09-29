import bs4
import functools

import efictopub.models


class RedditComment:
    def __init__(self, praw_comment):
        self.praw_comment = praw_comment

        self.author_name = praw_comment.author.name if praw_comment.author else "[n/a]"
        self.author_flair_text = praw_comment.author_flair_text
        self.created_utc = praw_comment.created_utc
        self.edited = praw_comment.edited
        self.reddit_id = praw_comment.id
        self.permalink = praw_comment.permalink
        self.ups = praw_comment.ups

    @property
    @functools.lru_cache()
    def body_html(self):
        dom = bs4.BeautifulSoup(self.praw_comment.body_html, "lxml").body

        # Strip the containing <div> from the reddit comment.
        containing_div = dom.find("div", {"class": "md"})
        if containing_div:
            containing_div.unwrap()

        return dom.encode_contents().decode()

    @property
    @functools.lru_cache()
    def replies(self):
        return [RedditComment(c) for c in self.praw_comment.replies]

    @property
    @functools.lru_cache()
    def formatted_author_name(self):
        if self.author_flair_text:
            return f"{self.author_name} ({self.author_flair_text})"
        else:
            return self.author_name

    @functools.lru_cache()
    def as_comment(self):
        return efictopub.models.comment.Comment(
            author=self.formatted_author_name,
            date_published=self.created_utc,
            date_updated=self.edited,
            permalink=self.permalink,
            replies=[reply.as_comment() for reply in self.replies],
            score=self.ups,
            text=self.body_html,
        )
