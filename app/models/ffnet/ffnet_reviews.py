import bs4
import functools

from app.models.ffnet.ffnet_review import FFNetReview


class FFNetReviews:
    def __init__(self, html):
        self.html = bs4.BeautifulSoup(html, "lxml")

    @property
    @functools.lru_cache()
    def reviews(self):
        return [
            FFNetReview(td).as_comment()
            for td in self.html.select("#content_wrapper_inner")[0].find_all("td")
        ]
