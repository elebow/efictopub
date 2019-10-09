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
