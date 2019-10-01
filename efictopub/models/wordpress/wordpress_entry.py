import bs4
import functools
import re

from efictopub.models.chapter import Chapter
from efictopub.models.wordpress.wordpress_comment import WordpressComment


class WordpressEntry:
    def __init__(self, chapter_html):
        self.dom = bs4.BeautifulSoup(chapter_html, "lxml")

    @property
    def comments(self):
        return [
            WordpressComment(element) for element in self.dom.select(".comment.depth-1")
        ]

    @property
    def date_published(self):
        meta_tag = self.dom.select("meta[property='article:published_time']")[0]
        return meta_tag.attrs["content"]

    @property
    def date_updated(self):
        meta_tag = self.dom.select("meta[property='article:modified_time']")[0]
        modified_time = meta_tag.attrs["content"]
        if modified_time != self.date_published:
            return modified_time

    @property
    def permalink(self):
        return self.dom.select("link[rel='canonical']")[0].attrs["href"]

    @property
    def next_url(self):
        links = self.dom.select("link[rel='next']")
        if links:
            return links[0].attrs["href"]
        return None

    @property
    @functools.lru_cache()
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
        if not isinstance(elem, bs4.element.NavigableString):
            elem_text = elem.text
        else:
            elem_text = elem
        return elem.name == "a" or re.match(r"^\s*$", elem_text)
