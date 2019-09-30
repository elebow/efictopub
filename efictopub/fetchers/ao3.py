import re

from efictopub.fetchers import BaseFetcher
from efictopub.models.story import Story


def can_handle_url(url):
    return re.search(r"(?:\w+:\/\/)?(?:www\.)?archiveofourown.org/works/\d+/.*", url)


class Fetcher(BaseFetcher):
    """Fetch story from archiveofourown.org"""

    def __init__(self, id_or_url):
        self.ao3_id = self.calculate_ao3_id(id_or_url)

    def fetch_story(self):
        ao3_chapters = self.fetch_chapters()
        title = ao3_chapters[0].story_title
        author = ao3_chapters[0].author_name
        return Story(
            title=title,
            author=author,
            summary=ao3_chapters[0].summary,
            chapters=[ch.as_chapter() for ch in ao3_chapters],
        )

    def calculate_ao3_id(self, id_or_url):
        if re.match(r"\d+$", id_or_url):
            return id_or_url

        matches = re.findall(
            r"(?:\w+:\/\/)?(?:www\.)?archiveofourown.org/works/(\d+)/.*", id_or_url
        )
        if matches:
            return matches[0]

        return None
