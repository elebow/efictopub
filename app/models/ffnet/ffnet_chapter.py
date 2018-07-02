import bs4
import functools
import html2text
import re

from app.models.chapter import Chapter


class FFNetChapter:
    def __init__(self, html):
        self.set_fields_from_html(html)

    def set_fields_from_html(self, html):
        dom = bs4.BeautifulSoup(html, "lxml")
        info_box = dom.select("#profile_top")[0]
        info_fields = info_box.select(".xcontrast_txt")

        self.author_name = info_fields[2].text.strip()
        self.title = dom.select("#chap_select")[0].find_all("option", selected=True)[0].text.strip()
        self.summary = info_fields[5]  # TODO do something with this

        matches = re.findall(
            r".*Favs:\s+([\d,]+).*Updated:.*?xutime=\"(\d+)\".*?Published:.*?xutime=\"(\d+)\".*?id:\s+(\d+)",
            str(info_fields[6]),
            re.DOTALL
        )[0]
        self.score = matches[0]
        self.date_updated = int(matches[1])
        self.date_published = int(matches[2])
        self.ffnet_id = matches[3]

        self.permalink = "https:" + dom.head.select("link[rel=canonical]")[0].attrs["href"]

        storytext_with_container = str(dom.select("#storytext")[0])
        # Yes, use regex to work with HTML. It's a very constrained input.
        storytext_html = re.sub(r"^<.*?>", "", storytext_with_container).replace("<\div>", "")
        text_maker = html2text.HTML2Text()
        text_maker.emphasis_mark = "*"
        self.text = text_maker.handle(storytext_html).strip()

        self.reviews = []  # TODO

    @functools.lru_cache()
    def as_chapter(self):
        return Chapter(author=self.author_name,
                       comments=self.reviews,
                       date_published=self.date_published,
                       date_updated=self.date_updated,
                       permalink=self.permalink,
                       score=self.score,
                       text=self.text,
                       title=self.title)
