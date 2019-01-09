import bs4
import functools
import re

from app.models.chapter import Chapter


class FFNetChapter:
    def __init__(self, chapter_html, reviews_htmls=[]):
        self.set_fields_from_html(chapter_html, reviews_htmls)

    def set_fields_from_html(self, chapter_html, reviews_htmls):
        self.dom = bs4.BeautifulSoup(chapter_html, "lxml")

        self.score_dates_id = str(self.get_info_fields()[6])

        self.text = self.dom.select("#storytext")[0].encode_contents().decode().strip()

        self.reviews = reviews_htmls

    @functools.lru_cache()
    def get_info_fields(self):
        info_box = self.dom.select("#profile_top")
        if not info_box:
            return ["unknown", "unknown", "unknown", "unknown", "unknown", "unknown", "unknown"]
        return info_box[0].select(".xcontrast_txt")

    def get_author_name(self):
        return self.get_info_fields()[2].text.strip()

    def get_chapter_title(self):
        select = self.dom.select("#chap_select")
        if select == []:
            return None
        return select[0].find_all("option", selected=True)[0].text.strip()

    def get_date_published(self):
        return int(re.search(r"Published:.*?xutime=\"(\d+)\"", self.score_dates_id, re.DOTALL).group(1))

    def get_date_updated(self):
        groups = re.search(r"Updated:.*?xutime=\"(\d+)\"", self.score_dates_id, re.DOTALL)
        if groups:
            return int(groups.group(1))
        else:
            return 0

    def get_permalink(self):
        canonical_links = self.dom.select("link[rel=canonical]")
        if canonical_links:
            return "https:" + canonical_links[0].attrs["href"]
        else:
            return None

    def get_score(self):
        return re.search(r"Favs:\s+([\d,]+)", self.score_dates_id, re.DOTALL).group(1)

    def get_story_title(self):
        return self.get_info_fields()[0].text.strip()

    def get_summary(self):
        # TODO do something with this
        return self.get_info_fields()[5].text.strip()

    @functools.lru_cache()
    def get_chapter_selector(self):
        return self.dom.select("#chap_select")

    def is_last_chapter(self):
        # Return True if the last chapter in the chapter selector is the one that is selected
        if self.is_single_chapter_story():
            return False

        select = self.get_chapter_selector()[0]
        chapters = [chap for chap in select.children
                    if isinstance(chap, bs4.element.Tag)]

        if len(chapters) == 1:
            return True

        return 'selected' in chapters[-1].attrs

    def is_single_chapter_story(self):
        return not self.get_chapter_selector()

    @functools.lru_cache()
    def as_chapter(self):
        return Chapter(author=self.get_author_name(),
                       comments=self.reviews,
                       date_published=self.get_date_published(),
                       date_updated=self.get_date_updated(),
                       permalink=self.get_permalink(),
                       score=self.get_score(),
                       story_title=self.get_story_title(),
                       text=self.text,
                       title=self.get_chapter_title())
