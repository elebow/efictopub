import bs4
from collections import namedtuple
import functools

ChapterData = namedtuple("ChapterData", ["url", "date"])


class AO3NavigationPage:
    def __init__(self, html):
        self.dom = bs4.BeautifulSoup(html, "lxml")

    @property
    @functools.lru_cache()
    def chapters(self):
        return [
            ChapterData(
                url=self.build_url(li.select("a")[0].attrs["href"]),
                date=li.select(".datetime")[0].text[1:-1],  # strip the parentheses
            )
            for li in self.dom.select(".chapter.index.group li")
        ]

    def build_url(self, path):
        return f"https://www.archiveofourown.org{path}"
