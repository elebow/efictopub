from datetime import datetime
import functools

from efictopub.models.chapter import Chapter


class SpacebattlesPost:
    def __init__(self, post_dom):
        self.dom = post_dom

    @property
    def author(self):
        return self.dom.select(".username")[0].text

    @property
    def date_published(self):
        # the first <time> element is for publish, even if there is an edit <time>
        return int(self.dom.select("time")[0].attrs["data-time"])

    @property
    def date_updated(self):
        edit_elems = self.dom.select(".message-lastEdit")
        if len(edit_elems) == 0:
            return 0
        return int(edit_elems[0].select("time")[0].attrs["data-time"])

    @property
    def permalink(self):
        # The second link in the right-side block is a permalink
        path = self.dom.select(".message-attribution-opposite a")[1].attrs["href"]
        return f"https://forums.spacebattles.com{path}"

    @property
    def likes(self):
        return int(self.dom.select(".sv-rating__count")[0].text)

    @property
    def text(self):
        return self.dom.select(".message-body")[0].encode_contents().decode().strip()

    @property
    def chapter_title(self):
        return self.dom.select(".threadmarkLabel")[0].text

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
