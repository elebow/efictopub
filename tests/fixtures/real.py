from app.models.chapter import Chapter
from app.models.comment import Comment


def chapter_real(n=0):
    return Chapter(comments=comments_real(3),
                   date_published=f"start_date {n}",
                   date_updated=f"end_date {n}",
                   permalink=f"permalink {n}",
                   author=f"great-author {n}",
                   score=5,
                   text=f"chapter {n}",
                   title=f"great-title {n}")


def chapters_real(count):
    return [chapter_real(n) for n in range(0, count)]


def comment_real(n):
    return Comment(author=f"author {n}",
                   date_published=f"published date {n}",
                   date_updated=f"updated date {n}",
                   permalink=f"permalink {n}",
                   replies=[comment_real(m) for m in range(0, n - 1)] if n > 0 else [],
                   score=f"score {n}",
                   text=f"text {n}")


def comments_real(count):
    return [comment_real(n) for n in range(0, count)]


def ffnet_chapter_html_real():
    with open("tests/fixtures/www.fanfiction.net_1.html", "rb") as file:
        return file.read()


def ffnet_chapter_2_html_real():
    with open("tests/fixtures/www.fanfiction.net_2.html", "rb") as file:
        return file.read()


def praw_submissions_real():
    import pickle
    with open("tests/fixtures/array_of_3_submissions_with_comments.pickle", "rb") as file:
        return pickle.load(file)


def find_praw_submission_real(_self=None, *, url=None, id=None):
    if url is not None:
        return [subm for subm in praw_submissions_real() if subm.url == url][0]
    elif id is not None:
        return [subm for subm in praw_submissions_real() if subm.id == id][0]
