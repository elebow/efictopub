import bs4
import functools
import re

from efictopub.models.chapter import Chapter


class SpacebattlesPost:
    def __init__(self, post_html):
        self.dom = bs4.BeautifulSoup(post_html, "lxml")

    @functools.lru_cache()
    def as_chapter(self):
        return Chapter(
            comments=[],
            date_published=self.date_published,
            date_updated=self.date_updated,
            permalink=self.permalink,
            score=None,
            text=self.text,
            title=self.chapter_title,
        )
