import bs4
from datetime import datetime
import functools
import re

from efictopub.models.chapter import Chapter


class RoyalroadChapter:
    def __init__(self, html, comments_html):
        self.dom = bs4.BeautifulSoup(html, "lxml")
        # TODO comments

    @property
    def author_name(self):
        return self.dom.select(".profile-info h1")[0].text.strip()

    @property
    def date_published(self):
        return int(self.dom.select(".profile-info time")[0].attrs["unixtime"])

    @property
    def comments(self):
        # TODO
        return []

    @property
    def permalink(self):
        return self.dom.select("meta[property='og:url']")[0].attrs["content"]

    @property
    def score(self):
        rating_classes = self.dom.select(".star")[0].attrs["class"]
        star_class = [c for c in rating_classes if c.startswith("star-")][0]
        rating = int(star_class.split("-")[1]) / 10

        return rating

    @property
    def summary(self):
        return None  # Royal Road doesn't have per-chapter summaries

    @property
    def text(self):
        return (
            self.author_note_top
            + self.dom.select(".chapter-content")[0].encode_contents().decode().strip()
            + self.author_note_bottom
        )

    @property
    def author_note_top(self):
        elems = self.dom.select(".author-note-portlet")
        if elems:
            return elems[0].encode_contents().decode().strip()
        return ""

    @property
    def author_note_bottom(self):
        elems = self.dom.select(".author-note")
        if elems:
            return elems[0].encode_contents().decode().strip()
        return ""

    @property
    def title(self):
        return self.dom.select(".fic-header h1")[0].text

    @functools.lru_cache()
    def as_chapter(self):
        return Chapter(
            comments=self.comments,
            date_published=self.date_published,
            date_updated=0,  # TODO
            permalink=self.permalink,
            score=self.score,
            text=self.text,
            title=self.title,
        )
