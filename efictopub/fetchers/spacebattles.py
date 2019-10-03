import bs4
import functools
import re

from efictopub import config
from efictopub.fetchers import BaseFetcher
from efictopub.lib import request_dispatcher
from efictopub.models.story import Story
from efictopub.models.spacebattles.spacebattles_post import SpacebattlesPost


def can_handle_url(url):
    return re.search(r"^(?:\w+:\/\/)forums\.spacebattles.com", url)


class SpacebattlesPage:
    def __init__(self, dom):
        self.dom = dom

    @property
    def messages(self):
        return self.dom.select(".message")

    @property
    def next_page_url(self):
        links = self.dom.select("link[rel='next']")
        if links:
            return links[0].attrs["href"]
        return None


class Fetcher(BaseFetcher):
    """Fetch story from Spacebattles.com thread(s)"""

    def __init__(self, id_or_url):
        self.thread_id = self.calculate_thread_id(id_or_url)

    def fetch_story(self):
        title = config.get_fetcher_opt("title", required=True)
        posts = list(self.fetch_posts())
        author = posts[0].author
        return Story(
            title=title,
            author=author,
            summary="",
            chapters=[entry.as_chapter() for entry in posts],
        )

    def fetch_posts(self):
        return list(self.generate_threadmarked_posts())

    def generate_threadmarked_posts(self, category=1):
        url = self.threadmarks_reader_url
        while True:
            print(f"Fetching posts from page")
            html = request_dispatcher.get(url).text
            page = SpacebattlesPage(bs4.BeautifulSoup(html, "lxml"))

            for message in page.messages:
                yield SpacebattlesPost(message)

            url = page.next_page_url
            if not url:
                print("Done. Reached end of last page")
                return

    def calculate_thread_id(self, id_or_url):
        if re.match(r"^\d+$", id_or_url):
            return id_or_url

        matches = re.findall(
            r".*://forums.spacebattles.com/threads/(?:[^/]*\.)?(\d+)", id_or_url
        )
        if matches:
            return matches[0]

        return None

    @property
    @functools.lru_cache()
    def threadmarks_categories(self):
        # We can get the threadmarks categories from any thread page, but there is no page that is guaranteed to be included in all fetcher modes.
        # So, just get them from the threadmarks index page for the default category
        html = request_dispatcher.get(self.threadmarks_index_url).text
        dom = bs4.BeautifulSoup(html, "lxml")
        tabs = dom.select(".threadmarks .tabs li")
        return {
            tab.text.strip().lower(): tab.find("a").attrs["href"].split("=")[-1]
            for tab in tabs
        }

    @property
    def thread_base_url(self):
        return f"https://forums.spacebattles.com/threads/{self.thread_id}"

    @property
    def threadmarks_index_url(self, category=1):
        return f"{self.thread_base_url}/threadmarks?category_id={category}"

    @property
    def threadmarks_reader_url(self, category=1):
        return f"{self.thread_base_url}/{category}/reader"
