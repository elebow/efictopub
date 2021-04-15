import functools
import re

from efictopub import config
from efictopub.fetchers import BaseFetcher
from efictopub.lib import request_dispatcher
from efictopub.models.royalroad.royalroad_chapter import RoyalroadChapter
from efictopub.models.royalroad.royalroad_index_page import RoyalroadIndexPage
from efictopub.models.story import Story


def can_handle_url(url):
    return re.search(r"^(?:\w+:\/\/)?(?:www\.)?royalroad.com/fiction/\d+(?:/.*)?", url)


class Fetcher(BaseFetcher):
    """Fetch story from royalroad.com"""

    def __init__(self, id_or_url):
        self.rr_id = self.calculate_rr_id(id_or_url)

    def fetch_story(self):
        return Story(
            title=self.story_index.title,
            author=self.story_index.author,
            summary=self.story_index.summary,
            chapters=[ch.as_chapter() for ch in self.fetch_chapters()],
        )

    def fetch_chapters(self):
        return list(self.generate_rr_chapters())

    def generate_rr_chapters(self):
        for chapter_url in self.story_index.chapter_urls:
            print(f"Fetching chapter {chapter_url}")
            chapter_html = request_dispatcher.get(chapter_url)

            if config.get("comments") != "none":
                comments_html = ""  # TODO
            else:
                comments_html = ""

            rr_chapter = RoyalroadChapter(str(chapter_html), str(comments_html))

            print("OK")
            yield rr_chapter

    @property
    @functools.lru_cache()
    def story_index(self):
        index_page_html = request_dispatcher.get(
            f"https://www.royalroad.com/fiction/{self.rr_id}"
        )

        return RoyalroadIndexPage(index_page_html)

    def calculate_rr_id(self, id_or_url):
        if re.match(r"\d+$", id_or_url):
            return id_or_url

        matches = re.findall(
            r"(?:\w+:\/\/)?(?:www\.)?royalroad.com/fiction/(\d+)(?:/)?.*", id_or_url
        )
        if matches:
            return matches[0]

        return None
