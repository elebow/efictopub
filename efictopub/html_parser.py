import bs4
import functools
import re


class HTMLParser:
    class Link:
        def __init__(self, a):
            self.href = a.attrs.get("href")
            self.text = a.text
            self.title = a.attrs.get("title")

    def __init__(self, src):
        self.dom = bs4.BeautifulSoup(src, "lxml")

    @property
    @functools.lru_cache()
    def a_elements(self):
        return self.dom.select("a")

    def as_html(self):
        self.dom.encode()

    def links_containing_text(self, text_to_find):
        """Return all the links contaning a specified string.
        This is useful for finding prev/next links in a post that is part of a series.
        """
        regexp_to_find = re.compile(r"\b%s\b" % text_to_find, re.IGNORECASE)
        return [self.Link(a) for a in self.a_elements if regexp_to_find.search(a.text)]
