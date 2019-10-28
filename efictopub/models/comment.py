from datetime import datetime

from efictopub.lib import comment_pruner


class Comment:
    """
    A comment on a chapter.
    """

    def __init__(
        self, *, author, date_published, date_updated, permalink, replies, score, text
    ):
        self.author = author
        self.date_published = date_published
        self.date_updated = date_updated
        self.permalink = permalink
        self.replies = replies
        self.score = score
        self.text = text

    def tree_containing_author(self, author_name):
        return comment_pruner.tree_containing_author(self, author_name)

    def pretty_author(self):
        if self.date_updated:
            readable_date_updated = datetime.utcfromtimestamp(
                self.date_updated
            ).strftime("%Y-%m-%d")
            edited_string = f", edited {readable_date_updated}"
        else:
            edited_string = ""
        readable_date = datetime.utcfromtimestamp(self.date_published).strftime(
            "%Y-%m-%d"
        )
        return f"{self.author} ({readable_date}{edited_string})"

    def as_html(self):
        author = f"<p>{self.pretty_author()}</p>"
        body = f"<p>{self.text}</p>"
        if self.replies:
            replies = (
                "<div class='replies'>"
                + "".join([reply.as_html() for reply in self.replies])
                + "</div>"
            )
        else:
            replies = ""
        return f"<div class='comment'>{author}{body}{replies}</div>"

    def as_dict(self):
        attr_names = [
            "author",
            "date_published",
            "date_updated",
            "permalink",
            "replies",
            "score",
            "text",
        ]
        mapping = {name: getattr(self, name) for name in attr_names}
        return mapping

    @classmethod
    def from_dict(cls, mapping):
        return cls(
            author=mapping["author"],
            date_published=mapping["date_published"],
            date_updated=mapping["date_updated"],
            permalink=mapping["permalink"],
            replies=mapping["replies"],
            score=mapping["score"],
            text=mapping["text"],
        )
