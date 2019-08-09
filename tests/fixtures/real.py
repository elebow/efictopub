from app.models.chapter import Chapter
from app.models.comment import Comment


def chapter_real(n=0):
    return Chapter(
        comments=comments_real(3),
        date_published=f"start_date {n}",
        date_updated=f"end_date {n}",
        permalink=f"permalink {n}",
        score=5,
        text=f"chapter {n}",
        title=f"great-title {n}",
    )


def chapters_real(count):
    return [chapter_real(n) for n in range(0, count)]


def comment_real(n):
    return Comment(
        author=f"author {n}",
        date_published=f"published date {n}",
        date_updated=f"updated date {n}",
        permalink=f"permalink {n}",
        replies=[comment_real(m) for m in range(0, n - 1)] if n > 0 else [],
        score=f"score {n}",
        text=f"text {n}",
    )


def comments_real(count):
    return [comment_real(n) for n in range(0, count)]


def ffnet_chapter_html_real():
    with open("tests/fixtures/www.fanfiction.net_1.html", "r") as file:
        return file.read()


def ffnet_chapter_2_html_real():
    with open("tests/fixtures/www.fanfiction.net_2.html", "r") as file:
        return file.read()


def ffnet_chapter_3_html_real():
    with open("tests/fixtures/www.fanfiction.net_3.html", "r") as file:
        return file.read()


def ffnet_chapter_reviews_html_real():
    with open("tests/fixtures/www.fanfiction.net_reviews.html", "r") as file:
        return file.read()


def ffnet_single_chapter_story_html_real():
    with open("tests/fixtures/www.fanfiction.net_single.html", "r") as file:
        return file.read()


def ffnet_single_chapter_story_reviews_html_real():
    with open("tests/fixtures/www.fanfiction.net_single_reviews.html", "r") as file:
        return file.read()
