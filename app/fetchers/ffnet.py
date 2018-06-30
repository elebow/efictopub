import re
import requests

from app import fetchers
from app.models.ffnet.ffnet_chapter import FFNetChapter
from app.models.story import Story


class FFNet(fetchers.BaseFetcher):
    """Fetch story from fanfiction.net"""

    def __init__(self, id_or_url):
        self.story_base_url = self.calculate_story_base_url(id_or_url)

    def fetch_story(self):
        return Story(chapters=self.fetch_chapters())

    def fetch_chapters(self):
        return [ffnet_chapter.as_chapter() for ffnet_chapter in self.generate_ffnet_chapters()]

    def generate_ffnet_chapters(self):
        return (FFNetChapter(html) for html in self.generate_htmls())

    def generate_htmls(self):
        for n in iter(int, 1):
            url = self.story_base_url + str(n)
            response = requests.get(url)
            if response.status_code == 404:
                return
            yield response.text

    def calculate_story_base_url(self, id_or_url):
        if re.match(r'\d+$', id_or_url):
            return f"https://www.fanfiction.net/s/{id_or_url}/"

        matches = re.findall(r"(.*//www.fanfiction.net/s/\d+/)\d+/.*", id_or_url)
        if matches:
            return matches[0]

        return None