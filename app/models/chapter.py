class Chapter:
    """
    A single installment of a series. Possibly the only installment.

    Fields:
        author          author's name string
        comments        list of Comment objects
        date_published  date the chapter was initially published
        date_updated    date the chapter was most recently updated
        permalink       permalink to the chapter
        score           score, if available. Reddit upvotes, ff.net favorites, etc.
        story_title     title of the story
        text            text content
        title           title of the chapter
    """

    def __init__(self, *,
                 author,
                 comments,
                 date_published,
                 date_updated,
                 permalink,
                 score,
                 story_title,
                 text,
                 title):
        self.author = author
        self.comments = comments
        self.date_published = date_published
        self.date_updated = date_updated
        self.permalink = permalink
        self.score = score
        self.story_title = story_title
        self.text = text
        self.title = title

    def as_dict(self):
        attr_names = ["author", "comments", "date_published", "date_updated", "permalink", "score",
                      "story_title", "text", "title"]
        mapping = {name: getattr(self, name) for name in attr_names}
        return mapping

    @classmethod
    def from_dict(cls, mapping):
        return cls(author=mapping["author"],
                   comments=mapping["comments"],
                   date_published=mapping["date_published"],
                   date_updated=mapping["date_updated"],
                   permalink=mapping["permalink"],
                   score=mapping["score"],
                   story_title=mapping["story_title"],
                   text=mapping["text"],
                   title=mapping["title"])
