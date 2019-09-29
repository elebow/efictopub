import bs4
import functools
import re

from efictopub.models.chapter import Chapter


class WordpressEntry:
    def __init__(self, chapter_html):
        self.dom = bs4.BeautifulSoup(chapter_html, "lxml")

    @property
    def comments(self):
        return []
        return self.dom.select("#storytext")[0].encode_contents().decode().strip()

    @property
    def date_published(self):
        pass

    @property
    def date_updated(self):
        pass

    @property
    def permalink(self):
        pass

    @property
    def text(self):
        article = self.dom.select(".entry-content")[0]

        for element in article.select("#jp-post-flair"):
            element.extract()
        for comment in article.find_all(text=lambda x: isinstance(x, bs4.Comment)):
            comment.extract()
        for p in article.select("p"):
            # any paragraph that is nothing but links and whitespace is probably navigation
            if all([self._element_is_whitespace_or_link(elem) for elem in p.contents]):
                p.extract()

        return article.encode_contents().decode().strip()

    @property
    def entry_title(self):
        return self.dom.select(".entry-title")[0].encode_contents().decode().strip()

    @functools.lru_cache()
    def as_chapter(self):
        return Chapter(
            comments=self.comments,
            date_published=self.date_published,
            date_updated=self.date_updated,
            permalink=self.permalink,
            score=None,  # Wordpress blogs don't have scores
            text=self.text,
            title=self.entry_title,
        )

    def _element_is_whitespace_or_link(self, elem):
        return elem.name == "a" or re.match(r"^\s*$", elem)
