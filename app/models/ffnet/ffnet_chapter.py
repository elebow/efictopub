import bs4
import functools
import html2text
import re

from app.models.chapter import Chapter


class FFNetChapter:
    def __init__(self, chapter_html, reviews_htmls=[]):
        self.set_fields_from_html(chapter_html, reviews_htmls)

    def set_fields_from_html(self, chapter_html, reviews_htmls):
        dom = bs4.BeautifulSoup(chapter_html, "lxml")
        info_box = dom.select("#profile_top")[0]
        info_fields = info_box.select(".xcontrast_txt")

        self.author_name = info_fields[2].text.strip()
        self.title = dom.select("#chap_select")[0].find_all("option", selected=True)[0].text.strip()
        self.story_title = info_fields[0].text.strip()
        self.summary = info_fields[5]  # TODO do something with this
        try:
            self.cover_image_url = info_box.select("img")[0].attrs["src"]  # TODO do something with this
        except IndexError:
            self.cover_image_url = ""

        self.score_dates_id = str(info_fields[6])

        storytext_with_container = str(dom.select("#storytext")[0])
        # Yes, use regex to work with HTML. It's a very constrained input.
        storytext_html = re.sub(r"^<.*?>", "", storytext_with_container).replace("<\div>", "")
        text_maker = html2text.HTML2Text()
        text_maker.emphasis_mark = "*"
        self.text = text_maker.handle(storytext_html).strip()

        self.reviews = reviews_htmls  # TODO convert to text

    def get_date_published(self):
        return int(re.search(r"Published:.*?xutime=\"(\d+)\"", self.score_dates_id, re.DOTALL).group(1))

    def get_date_updated(self):
        # TODO doesn't always exist
        return int(re.search(r"Updated:.*?xutime=\"(\d+)\"", self.score_dates_id, re.DOTALL).group(1))

    def get_permalink(self):
        canonical_links = self.dom.head.select("link[rel=canonical]")
        if canonical_links:
            return "https:" + canonical_links[0].attrs["href"]
        else:
            return None

    def get_score(self):
        return re.search(r"Favs:\s+([\d,]+)", self.score_dates_id, re.DOTALL).group(1)

    @functools.lru_cache()
    def as_chapter(self):
        return Chapter(author=self.author_name,
                       comments=self.reviews,
                       date_published=self.get_date_published(),
                       date_updated=self.get_date_updated(),
                       permalink=self.get_permalink(),
                       score=self.get_score(),
                       story_title=self.story_title,
                       text=self.text,
                       title=self.title)
