import re

from efictopub import config
from efictopub.fetchers import BaseFetcher
from efictopub.lib import request_dispatcher
from efictopub.models.story import Story
from efictopub.models.wordpress.wordpress_entry import WordpressEntry


def can_handle_url(url):
    return re.search(r"(?:\w+:\/\/).+\.wordpress.com", url)


class Fetcher(BaseFetcher):
    """Fetch story from arbitrary WordPress blog"""

    def __init__(self, url):
        self.first_chapter_url = url

    def fetch_story(self):
        title = config.get_fetcher_opt("title", required=True)
        author = config.get_fetcher_opt("author", required=True)
        return Story(
            title=title,
            author=author,
            summary="",
            chapters=[ch.as_chapter() for ch in self.fetch_blog_entries()],
        )

    def fetch_blog_entries(self):
        return list(self.generate_next_entries(self.first_chapter_url))

    def generate_next_entries(self, start_url):
        """Generate wordpress.Entry objects by following "next" links."""
        chapter_url = start_url
        while True:
            print(f"Fetching chapter {chapter_url}")
            entry_html = request_dispatcher.get(chapter_url).text
            entry = WordpressEntry(entry_html)
            print("OK")

            yield entry

            if self.is_last_chapter_url(chapter_url):
                print("Done. Matched last_chapter pattern.")
                return

            chapter_url = entry.next_url
            if not chapter_url:
                print("Done. Could not find a `next` link.")
                return

    def is_last_chapter_url(self, url):
        last_chapter_pattern = config.get_fetcher_opt("last_chapter_pattern")
        return last_chapter_pattern and re.search(last_chapter_pattern, url)
