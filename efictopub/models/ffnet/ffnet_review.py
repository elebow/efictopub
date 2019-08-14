from datetime import datetime
import functools

import efictopub.models.comment


class FFNetReview:
    def __init__(self, html):
        self.html = html

    @property
    @functools.lru_cache()
    def author_name(self):
        try:
            avatar_img = self.html.find_all("img")[-1]
        except IndexError:
            return None

        if avatar_img.next_sibling == " ":
            return avatar_img.next_sibling.next_sibling.text.strip()
        else:
            return avatar_img.next_sibling.strip()

    @property
    @functools.lru_cache()
    def date_published(self):
        try:
            # I'm not sure whether these are UTC or local, so assume UTC. Close enough.
            return datetime.utcfromtimestamp(
                int(self.html.select("span[data-xutime]")[0]["data-xutime"])
            )
        except IndexError:
            return None

    @property
    @functools.lru_cache()
    def text(self):
        return self.html.find("div").text

    @functools.lru_cache()
    def as_comment(self):
        return efictopub.models.comment.Comment(
            author=self.author_name,
            date_published=self.date_published,
            date_updated=None,
            permalink=None,
            replies=None,
            score=None,
            text=self.text,
        )
