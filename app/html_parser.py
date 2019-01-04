import bs4
import functools
from collections import namedtuple
import re


class HTMLParser:
    Link = namedtuple("Link", ["href", "text", "title"])

    def __init__(self, src):
        self.dom = bs4.BeautifulSoup(src, "lxml")

    @property
    @functools.lru_cache()
    def links(self):
        return [self.Link(href=a.attrs.get("href"), text=a.text, title=a.attrs.get("title"))
                for a
                in self.dom.select("a")]

    def as_html(self):
        self.dom.encode()

    def links_containing_text(self, text_to_find):
        """Return all the links contaning a specified string.
        This is useful for finding prev/next links in a post that is part of a series.
        """
        regexp_to_find = re.compile(r"\b%s\b" % text_to_find, re.IGNORECASE)
        return [link for link in self.links if regexp_to_find.search(link.text)]
