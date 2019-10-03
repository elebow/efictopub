from datetime import datetime
import functools
import re

from efictopub.models.chapter import Chapter


class SpacebattlesPost:
    def __init__(self, post_dom):
        self.dom = post_dom

    @property
    def author(self):
        return self.dom.select(".messageUserBlock .username")[0].text

    @property
    def date_published(self):
        date_str = self.dom.select(".messageMeta .DateTime")[0].attrs["title"]
        return datetime.strptime(date_str, "%b %d, %Y at %I:%M %p").timestamp()

    @property
    def date_updated(self):
        date_str = self.dom.select(".editDate .DateTime")[0].attrs["title"]
        return datetime.strptime(date_str, "%b %d, %Y at %I:%M %p").timestamp()

    @property
    def permalink(self):
        path = self.dom.select(".messageMeta .hashPermalink")[0].attrs["href"]
        return f"https://forums.spacebattles.com/{path}"

    @property
    def likes(self):
        # add 3 for the first three names before the "and N others"
        return (
            int(self.dom.select(".LikeText")[0].find_all("a")[-1].text.split(" ")[0])
            + 3
        )

    @property
    def text(self):
        return self.dom.select(".messageText")[0].encode_contents().decode().strip()

    @property
    def chapter_title(self):
        elem_text = self.dom.select(".threadmarker .label")[0].text
        return elem_text.strip().replace(r"Threadmarks: ", "")

    @functools.lru_cache()
    def as_chapter(self):
        return Chapter(
            comments=[],
            date_published=self.date_published,
            date_updated=self.date_updated,
            permalink=self.permalink,
            score=self.likes,
            text=self.text,
            title=self.chapter_title,
        )
