from doubles import InstanceDouble
import praw


def chapter_double(n=0):
    return InstanceDouble("app.models.chapter.Chapter",
                          comments=comments_double(3),
                          date_published=f"start date {n}",
                          date_updated=f"end date {n}",
                          permalink=f"permalink {n}",
                          author=f"great author {n}",
                          score=5,
                          text=f"chapter {n}",
                          title=f"great title {n}")


def chapters_double(count):
    return [chapter_double(n) for n in range(0, count)]


def comment_double(n=0):
    return InstanceDouble("app.models.comment.Comment",
                          author=f"author {n}",
                          date_published=f"published date {n}",
                          date_updated=f"updated date {n}",
                          permalink=f"permalink {n}",
                          replies=[comment_double(m) for m in range(0, n - 1)] if n > 0 else [],
                          score=f"score {n}",
                          text=f"text {n}")


def comments_double(count):
    return [comment_double(n) for n in range(0, count)]


def praw_redditor(n=0):
    return InstanceDouble("praw.models.Redditor",
                          name=f"redditor {n}")


def praw_comment_double(n=0, author="some author", body="some body text", replies=[]):
    return InstanceDouble("praw.models.reddit.comment.Comment",
                          author=author,
                          author_flair_text="",
                          body=body,
                          created_utc=f"created utc {n}",
                          edited=f"edited timestamp {n}",
                          id="reddit id {n}",
                          permalink=f"permalink {n}",
                          replies=replies,
                          ups=5)


def praw_submission_double(n=0, author=-1, comments=[], selftext="some selftext",
                           title="some title"):
    author = praw_redditor(n) if author == -1 else author
    # CommentForest is bothersome to mock. It needs to be iterable.
    comment_forest = praw.models.comment_forest.CommentForest(None, comments)
    return InstanceDouble("praw.models.Submission",
                          author=author,
                          comments=comment_forest,
                          created_utc=f"created utc {n}",
                          edited=f"edited timestamp {n}",
                          id="reddit id {n}",
                          permalink=f"permalink {n}",
                          selftext="aaa",
                          title=f"some title {n}",
                          ups=5)


def praw_submission_with_author_note_double(n=0):
    author = praw_redditor()
    comment = praw_comment_double(author=author, body="short author note")
    return praw_submission_double(author=author, comments=[comment])
    """
    # CommentForest is bothersome to mock. It needs to be iterable.
    comment_forest = praw.models.comment_forest.CommentForest(None, [comment])
    return InstanceDouble("praw.models.Submission",
                          author=author,
                          comments=comment_forest,
                          created_utc=f"created utc {n}",
                          edited=f"edited timestamp {n}",
                          id="reddit id {n}",
                          permalink=f"permalink {n}",
                          selftext="aaa",
                          title=f"some title {n}",
                          ups=5)
    """


def praw_submission_continued_in_comments_double(n=0):
    author = praw_redditor()
    comment2 = praw_comment_double(author=author,
                                   body="long continuation 2" * 200,
                                   replies=[])
    comment1 = praw_comment_double(author=author,
                                   body="long continuation 1" * 200,
                                   replies=[comment2])
    comment_forest = praw.models.comment_forest.CommentForest(None, [comment1])
    return InstanceDouble("praw.models.Submission",
                          author=author,
                          comments=comment_forest,
                          created_utc=f"created utc {n}",
                          edited=f"edited timestamp {n}",
                          id="reddit id {n}",
                          permalink=f"permalink {n}",
                          selftext="aaa",
                          title=f"some title {n}",
                          ups=5)
