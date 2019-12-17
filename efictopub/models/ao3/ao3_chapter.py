import bs4
from datetime import datetime
import functools
import re

from efictopub.models.chapter import Chapter


class AO3Chapter:
    def __init__(self, html, comments_html, *, date_published):
        self.dom = bs4.BeautifulSoup(html, "lxml")
        # TODO comments

        # The markup contains some invisible elements that we don't want in the output
        for landmark in self.dom.select(".landmark"):
            landmark.decompose()

        # AO3 doesn't show date published on the chapter page, so we have to take it as an argument
        self.date_published = datetime.strptime(date_published, "%Y-%m-%d").timestamp()

    @property
    def author_name(self):
        return self.dom.select(".byline")[0].text.strip()

    @property
    def comments(self):
        # TODO
        return []

    @property
    def permalink(self):
        # TODO AO3 treats single- and multi-chapter works differently
        return f"https://www.archiveofourown.org/chapters/{self.ao3_id}"

    @property
    def score(self):
        return int(self.dom.select(".stats dd.kudos")[0].text)

    @property
    def story_title(self):
        return self.dom.select(".title.heading")[0].text.strip()

    @property
    def summary(self):
        return self.dom.select(".summary .userstuff")[0].text.strip()

    @property
    def text(self):
        # TODO concatenate the author notes and similar fields
        return (
            self.dom.select(".module[role=article]")[0]
            .encode_contents()
            .decode()
            .strip()
        )

    @property
    def title(self):
        title_line = self.dom.select(".chapter.preface .title")[0].text
        matches = re.findall(r".*: (.*)", title_line)
        if matches:
            return matches[0].strip()
        return title_line.strip()

    @property
    def ao3_id(self):
        # TODO AO3 treats single- and multi-chapter works differently
        return self.dom.select("#selected_id option[selected=selected]")[0].attrs[
            "value"
        ]

    @functools.lru_cache()
    def as_chapter(self):
        return Chapter(
            comments=self.comments,
            date_published=self.date_published,
            date_updated=0,  # AO3 doesn't show a chapter's updated date anywhere
            permalink=self.permalink,
            score=self.score,
            text=self.text,
            title=self.title,
        )
