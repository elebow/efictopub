import itertools
import functools
import re

from efictopub import config
from efictopub.fetchers import BaseFetcher
from efictopub.lib import request_delay
from efictopub.models.ffnet.ffnet_chapter import FFNetChapter
from efictopub.models.story import Story


def can_handle_url(url):
    return re.search(r"(?:\w+:\/\/)?www.fanfiction.net/", url)


class Fetcher(BaseFetcher):
    """Fetch story from fanfiction.net"""

    def __init__(self, id_or_url):
        self.ffnet_id = self.calculate_ffnet_id(id_or_url)

    def fetch_story(self):
        ffn_chapters = self.fetch_chapters()
        title = ffn_chapters[0].story_title
        author = ffn_chapters[0].author_name
        return Story(
            title=title,
            author=author,
            summary=ffn_chapters[0].summary,
            chapters=[ch.as_chapter() for ch in ffn_chapters],
        )

    def fetch_chapters(self):
        return list(self.generate_ffnet_chapters())

    def generate_ffnet_chapters(self):
        for n in itertools.count(1):
            chapter_url = self.generate_chapter_url(n)

            print(f"Fetching chapter {n} ({chapter_url})")
            chapter_html = request_delay.get(chapter_url).text

            if config.get("fetch_comments", bool):
                reviews_url = self.generate_chapter_reviews_url(n)
                print(f"Fetching chapter {n} reviews ({reviews_url})")
                reviews_html = request_delay.get(reviews_url).text
            else:
                reviews_html = ""

            ffnet_chapter = FFNetChapter(str(chapter_html), str(reviews_html))

            print("OK")
            yield ffnet_chapter

            if (
                ffnet_chapter.is_last_chapter()
                or ffnet_chapter.is_single_chapter_story()
            ):
                print("Done")
                return

    def calculate_ffnet_id(self, id_or_url):
        if re.match(r"\d+$", id_or_url):
            return id_or_url

        matches = re.findall(r".*//www.fanfiction.net/s/(\d+)/\d+/.*", id_or_url)
        if matches:
            return matches[0]

        return None

    @functools.lru_cache()
    def generate_chapter_url(self, n):
        return f"https://www.fanfiction.net/s/{self.ffnet_id}/{n}"

    @functools.lru_cache()
    def generate_chapter_reviews_url(self, n):
        # Reviews are not paginated, it seems. The pattern is always
        # https://www.fanfiction.net/r/{story_id}/{chap_num}/1/
        return f"https://www.fanfiction.net/r/{self.ffnet_id}/{n}/1/"
