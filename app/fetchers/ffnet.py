import itertools
import functools
import re

from app import fetchers
from app.lib import request_delay
from app.models.ffnet.ffnet_chapter import FFNetChapter
from app.models.story import Story


def can_handle_url(url):
    return re.search(r"(?:\w+:\/\/)?www.fanfiction.net/", url)


class FFNet(fetchers.BaseFetcher):
    """Fetch story from fanfiction.net"""

    def __init__(self, id_or_url):
        self.ffnet_id = self.calculate_ffnet_id(id_or_url)

    def fetch_story(self):
        return Story(chapters=self.fetch_chapters())

    def fetch_chapters(self):
        return [ffnet_chapter.as_chapter() for ffnet_chapter in self.generate_ffnet_chapters()]

    def generate_ffnet_chapters(self):
        return (FFNetChapter(chapter_html, reviews_html)
                for chapter_html, reviews_html
                in zip(self.generate_chapter_htmls(), self.generate_review_htmls()))

    def generate_chapter_htmls(self):
        for n in itertools.count(1):
            url = f"{self.get_story_base_url()}/{n}"
            print(f"Fetching chapter {n} ({url})")
            response = request_delay.get(url)
            if "FanFiction.Net Message Type 1<hr size=1 noshade>Chapter not found." in str(response.text):
                print("Done")
                return
            print("OK")
            yield response.text

    def generate_review_htmls(self):
        for n in itertools.count(1):
            # Reviews are not paginated, it seems. The pattern is always
            # https://www.fanfiction.net/r/{story_id}/{chap_num}/1/
            url = f"{self.get_story_base_url()}/{n}/1/"

            print(f"Fetching chapter {n} reviews ({url})")
            response = request_delay.get(url)
            if "<td  style='padding-top:10px;padding-bottom:10px'>No Reviews found.</td>" \
                    in str(response.text):
                print("Done")
                return
            print("OK")
            yield response.text

    def calculate_ffnet_id(self, id_or_url):
        if re.match(r"\d+$", id_or_url):
            return id_or_url

        matches = re.findall(r".*//www.fanfiction.net/s/(\d+)/\d+/.*", id_or_url)
        if matches:
            return matches[0]

        return None

    @functools.lru_cache()
    def get_story_base_url(self):
        return f"https://www.fanfiction.net/s/{self.ffnet_id}"

    @functools.lru_cache()
    def get_review_base_url(self):
        return f"https://www.fanfiction.net/r/{self.ffnet_id}"


FETCHER_CLASS = FFNet
