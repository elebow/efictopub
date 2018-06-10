import functools

from app.markdown_parser import MarkdownParser


class Comment:
    def __init__(self, praw_comment):
        self.author_name = praw_comment.author.name if praw_comment.author else "[n/a]"
        self.author_flair_text = praw_comment.author_flair_text
        self.body = praw_comment.body
        self.created_utc = praw_comment.created_utc
        self.edited = praw_comment.edited
        self.reddit_id = praw_comment.id
        self.replies = self.replies_for_comment(praw_comment)
        self.permalink = praw_comment.permalink
        self.ups = praw_comment.ups

    def replies_for_comment(self, praw_comment):
        return [Comment(c) for c in praw_comment.replies]

    def all_links_in_text(self):
        return MarkdownParser(self.body).links

    @functools.lru_cache()
    def as_dict(self):
        attr_names = ["author_name", "author_flair_text", "body", "created_utc", "edited", "reddit_id",
                      "permalink", "ups"]
        attrs = {name: getattr(self, name) for name in attr_names}
        attrs["replies"] = [reply.as_dict() for reply in self.replies]
        return attrs
