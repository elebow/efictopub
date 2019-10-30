from datetime import datetime
import functools

from efictopub.models.comment import Comment


class WordpressComment:
    def __init__(self, comment_element):
        self.comment_body = comment_element.find("article")

        # We only want the immediate child comments of this comment
        self.comment_replies = comment_element.select(
            f"#{comment_element.attrs['id']} > .children > .comment"
        )

    @property
    def author(self):
        return self.comment_body.select(".comment-author .fn")[0].text

    @property
    def text(self):
        return (
            self.comment_body.select(".comment-content")[0]
            .encode_contents()
            .decode()
            .strip()
        )

    @property
    def replies(self):
        return [WordpressComment(reply) for reply in self.comment_replies]

    @property
    def date(self):
        return datetime.strptime(
            self.comment_body.find("time").attrs["datetime"], "%Y-%m-%dT%H:%M:%S%z"
        ).timestamp()

    @functools.lru_cache()
    def as_comment(self):
        return Comment(
            author=self.author,
            date_published=self.date,
            date_updated=None,
            permalink=None,
            replies=[reply.as_comment() for reply in self.replies],
            score=None,
            text=self.text,
        )
