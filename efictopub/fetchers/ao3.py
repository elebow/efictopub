import re

from efictopub import config
from efictopub.fetchers import BaseFetcher
from efictopub.lib import request_dispatcher
from efictopub.models.ao3.ao3_chapter import AO3Chapter
from efictopub.models.ao3.ao3_navigation_page import AO3NavigationPage
from efictopub.models.story import Story


def can_handle_url(url):
    return re.search(
        r"^(?:\w+:\/\/)?(?:www\.)?archiveofourown.org/works/\d+(?:/.*)?", url
    )


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

    def fetch_chapters(self):
        return list(self.generate_ao3_chapters())

    def generate_ao3_chapters(self):
        for chapter_info in self.fetch_chapters_info():
            chapter_url = chapter_info.url

            print(f"Fetching chapter {chapter_url}")
            chapter_html = request_dispatcher.get(chapter_url).text

            if config.get("comments") != "none":
                comments_html = ""  # TODO
            else:
                comments_html = ""

            ao3_chapter = AO3Chapter(
                str(chapter_html), str(comments_html), date_published=chapter_info.date
            )

            print("OK")
            yield ao3_chapter

    def fetch_chapters_info(self):
        navigation_page_url = (
            f"https://www.archiveofourown.org/works/{self.ao3_id}/navigate"
        )
        navigation_page_html = request_dispatcher.get(navigation_page_url).text
        ao3_navigation_page = AO3NavigationPage(navigation_page_html)

        return ao3_navigation_page.chapters

    def calculate_ao3_id(self, id_or_url):
        if re.match(r"\d+$", id_or_url):
            return id_or_url

        matches = re.findall(
            r"(?:\w+:\/\/)?(?:www\.)?archiveofourown.org/works/(\d+)(?:/)?.*", id_or_url
        )
        if matches:
            return matches[0]

        return None
