import re

from efictopub.fetchers import BaseFetcher
from efictopub.html_parser import HTMLParser
from efictopub.lib import request_dispatcher
from efictopub.models.story import Story
from efictopub.models.wordpress.wordpress_entry import WordpressEntry
from efictopub.exceptions import AmbiguousNextError


def can_handle_url(url):
    return re.search(r"(?:\w+:\/\/).+\.wordpress.com", url)


class Fetcher(BaseFetcher):
    """Fetch story from arbitrary WordPress blog"""

    def __init__(self, url):
        self.first_chapter_url = url
        self.last_chapter_pattern = "TODO"
        # CLI arg that passes through to the fetcher. Get via config?

    def fetch_story(self):
        title = ""
        author = ""
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

            if re.search(self.last_chapter_pattern, chapter_url):
                print("Done. Matched last_chapter pattern.")
                return

            chapter_url = entry.next_url
            if not chapter_url:
                print("Done. Could not find a `next` link.")
                return
