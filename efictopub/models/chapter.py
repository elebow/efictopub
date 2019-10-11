from efictopub import config


class Chapter:
    """
    A single installment of a series. Possibly the only installment.

    Fields:
        comments        list of Comment objects
        date_published  date the chapter was initially published
        date_updated    date the chapter was most recently updated
        permalink       permalink to the chapter
        score           score, if available. Reddit upvotes, ff.net favorites, etc.
        text            text content
        title           title of the chapter
    """

    def __init__(
        self, *, comments, date_published, date_updated, permalink, score, text, title
    ):
        self.comments = self.prune_comments(comments)
        self.date_published = date_published
        self.date_updated = date_updated
        self.permalink = permalink
        self.score = score
        self.text = text
        self.title = title

    def prune_comments(self, comments):
        author_only_name = config.get_fetcher_opt("author_only_replies")
        new_comments = [
            comment.tree_containing_author(author_only_name)
            if author_only_name
            else comment
            for comment in comments
        ]
        return list(filter(None, new_comments))

    def as_dict(self):
        attr_names = [
            "comments",
            "date_published",
            "date_updated",
            "permalink",
            "score",
            "text",
            "title",
        ]
        mapping = {name: getattr(self, name) for name in attr_names}
        return mapping

    @classmethod
    def from_dict(cls, mapping):
        return cls(
            comments=mapping["comments"],
            date_published=mapping["date_published"],
            date_updated=mapping["date_updated"],
            permalink=mapping["permalink"],
            score=mapping["score"],
            text=mapping["text"],
            title=mapping["title"],
        )
