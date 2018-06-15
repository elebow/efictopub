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


def praw_submissions_real():
    import pickle
    with open("tests/fixtures/array_of_3_submissions_with_comments.pickle", "rb") as file:
        return pickle.load(file)
