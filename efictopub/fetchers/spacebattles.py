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


DOMAIN = "forums.spacebattles.com"


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
            return f"http://{DOMAIN}/{links[0].attrs['href']}"
        return None


class Fetcher(BaseFetcher):
    """Fetch story from Spacebattles.com thread(s)"""

    def __init__(self, id_or_url):
        self.thread_id = self.calculate_thread_id(id_or_url)

    def fetch_story(self):
        title = (
            config.get_fetcher_opt("title", required=True)
            + " ("
            + ", ".join(self.categories_to_fetch)
            + ")"
        )
        posts = list(self.fetch_posts())
        author = posts[0].author
        return Story(
            title=title,
            author=author,
            summary="",
            chapters=[entry.as_chapter() for entry in posts],
        )

    def fetch_posts(self):
        categories_posts = [
            self.generate_threadmarked_posts(category=category)
            for category in self.categories_to_fetch
        ]
        # TODO distinguish non-main-story chapters

        # First, compose all of the posts in category order.
        # All of category 1, followed by all of category 2, followed by ...
        posts_in_sequence = [post for category in categories_posts for post in category]

        if self.composition_order == "sequential":
            return posts_in_sequence
        elif self.composition_order == "chrono":
            # All threadmarked posts, regardless of category, ordered by post date
            return sorted(posts_in_sequence, key=lambda x: x.date_published)

    def generate_threadmarked_posts(self, *, category):
        category_id = self.threadmarks_categories[category]
        url = self.threadmarks_reader_url(category_id)
        while True:
            print(f"Fetching posts from page {url}")
            html = request_dispatcher.get(url).text
            page = SpacebattlesPage(bs4.BeautifulSoup(html, "lxml"))

            for message in page.messages:
                yield SpacebattlesPost(message)

            url = page.next_page_url
            if not url:
                print("Done. Reached end of last page")
                return

    @property
    def categories_to_fetch(self):
        requested_categories = config.get_fetcher_opt("categories", required=False)

        if requested_categories is None:
            # By default, include only the "threadmarks" category (the main story)
            return ["threadmarks"]
        elif requested_categories == "all":
            # The special value "all" means get everything
            return self.threadmarks_categories.keys()
        else:
            # else, split the input string by delimiters
            return re.split(r"[,\s]", requested_categories)

    @property
    def composition_order(self):
        requested_order = (
            config.get_fetcher_opt("order", required=False) or "sequential"
        )

        if requested_order not in ["sequential", "chrono"]:
            raise RuntimeError(f"Unknown order {requested_order}")

        return requested_order

    def calculate_thread_id(self, id_or_url):
        if re.match(r"^\d+$", id_or_url):
            return id_or_url

        matches = re.findall(fr".*://{DOMAIN}/threads/(?:[^/]*\.)?(\d+)", id_or_url)
        if matches:
            return matches[0]

        return None

    @property
    @functools.lru_cache()
    def threadmarks_categories(self):
        # We can get the threadmarks categories from any thread page, but there is no page that is guaranteed to be included in all fetcher modes.
        # So, just get them from the threadmarks index page for the default category
        url = self.threadmarks_index_url()
        print(f"Getting threadmarks categories from {url}")
        html = request_dispatcher.get(url).text
        dom = bs4.BeautifulSoup(html, "lxml")
        tabs = dom.select(".threadmarks .tabs li")
        return {
            tab.text.strip().lower(): tab.find("a").attrs["href"].split("=")[-1]
            for tab in tabs
        }

    @property
    def thread_base_url(self):
        return f"http://{DOMAIN}/threads/{self.thread_id}"

    def threadmarks_index_url(self, category_id=1):
        return f"{self.thread_base_url}/threadmarks?category_id={category_id}"

    def threadmarks_reader_url(self, category_id=1):
        return f"{self.thread_base_url}/{category_id}/reader"
