import bs4
import functools
import re

from app import config
from app.models.chapter import Chapter
from app.models.ffnet.ffnet_reviews import FFNetReviews


class FFNetChapter:
    def __init__(self, chapter_html, reviews_html=""):
        self.dom = bs4.BeautifulSoup(chapter_html, "lxml")
        self.reviews_html = reviews_html

    @property
    @functools.lru_cache()
    def info_fields(self):
        info_box = self.dom.select("#profile_top")
        if not info_box:
            return [
                "unknown",
                "unknown",
                "unknown",
                "unknown",
                "unknown",
                "unknown",
                "unknown",
            ]
        return info_box[0].select(".xcontrast_txt")

    @property
    def author_name(self):
        return self.info_fields[2].text.strip()

    @property
    def chapter_title(self):
        select = self.dom.select("#chap_select")
        if select == []:
            return None
        return select[0].find_all("option", selected=True)[0].text.strip()

    @property
    def score_dates_id(self):
        return str(self.info_fields[6])

    @property
    def date_published(self):
        return int(
            re.search(
                r"Published:.*?xutime=\"(\d+)\"", self.score_dates_id, re.DOTALL
            ).group(1)
        )

    @property
    def date_updated(self):
        groups = re.search(
            r"Updated:.*?xutime=\"(\d+)\"", self.score_dates_id, re.DOTALL
        )
        if groups:
            return int(groups.group(1))
        else:
            return 0

    @property
    def permalink(self):
        canonical_links = self.dom.select("link[rel=canonical]")
        if canonical_links:
            return "https:" + canonical_links[0].attrs["href"]
        else:
            return None

    @property
    def score(self):
        return re.search(r"Favs:\s+([\d,]+)", self.score_dates_id, re.DOTALL).group(1)

    @property
    def story_title(self):
        return self.info_fields[0].text.strip()

    @property
    def text(self):
        return self.dom.select("#storytext")[0].encode_contents().decode().strip()

    @property
    def summary(self):
        # TODO do something with this. New field on Chapter? On Story (and also move story_title)?
        return self.info_fields[5].text.strip()

    @property
    @functools.lru_cache()
    def reviews(self):
        if not config.get("fetch_comments", bool):
            return []

        if len(self.reviews_html) == 0:
            return []

        return FFNetReviews(self.reviews_html).reviews

    @property
    @functools.lru_cache()
    def chapter_selector(self):
        return self.dom.select("#chap_select")

    def is_last_chapter(self):
        # Return True if the last chapter in the chapter selector is the one that is selected
        if self.is_single_chapter_story():
            return False

        select = self.chapter_selector[0]
        chapters = [
            chap for chap in select.children if isinstance(chap, bs4.element.Tag)
        ]

        if len(chapters) == 1:
            return True

        return "selected" in chapters[-1].attrs

    def is_single_chapter_story(self):
        return not self.chapter_selector

    @functools.lru_cache()
    def as_chapter(self):
        return Chapter(
            author=self.author_name,
            comments=self.reviews,
            date_published=self.date_published,
            date_updated=self.date_updated,
            permalink=self.permalink,
            score=self.score,
            story_title=self.story_title,
            text=self.text,
            title=self.chapter_title,
        )
