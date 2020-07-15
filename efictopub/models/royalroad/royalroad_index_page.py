import bs4
from collections import namedtuple
import functools


class RoyalroadIndexPage:
    def __init__(self, html):
        self.dom = bs4.BeautifulSoup(html, "lxml")

    @property
    @functools.lru_cache()
    def chapter_urls(self):
        return [
            f"https://www.royalroad.com{tr.a.attrs['href']}"
            for tr in self.dom.select("#chapters tbody tr")
        ]

    @property
    @functools.lru_cache()
    def title(self):
        return self.dom.select(".fic-title h1")[0].text

    @property
    @functools.lru_cache()
    def author(self):
        return self.dom.select("meta[property='books:author']")[0].attrs["content"]

    @property
    @functools.lru_cache()
    def summary(self):
        return (
            self.dom.select("div[property='description']")[0]
            .encode_contents()
            .decode()
            .strip()
        )
