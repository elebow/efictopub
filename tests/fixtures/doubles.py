import praw

from doubles import InstanceDouble


def chapter_double(n=0, date_published=f"start date", date_updated=f"end date"):
    return InstanceDouble("app.models.chapter.Chapter",
                          comments=comments_double(3),
                          date_published=date_published,
                          date_updated=date_updated,
                          permalink=f"permalink {n}",
                          author=f"great author {n}",
                          score=5,
                          story_title="My Great Story",
                          text=f"chapter content {n}",
                          title=f"chapter title {n}")


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


def praw_redditor_with_submissions_double(name="some redditor"):
    return InstanceDouble("praw.models.Redditor",
                          name=name,
                          submissions=InstanceDouble("praw.models.listing.mixins.redditor.SubListing",
                                                     new=lambda: praw_submissions))


def praw_comment_double(n=0, author=praw_redditor(), body="some body text", replies=[]):
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


def praw_comments_double(count):
    return [praw_comment_double(n) for n in range(0, count)]


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
                          id=f"00000{n}",
                          permalink=f"https://www.reddit.com/r/great_subreddit/comments/00000{n}/great_title",
                          selftext=selftext,
                          title=title,
                          ups=5)


def praw_submission_with_author_note_double(n=0):
    author = praw_redditor()
    comment = praw_comment_double(author=author, body="short author note")
    return praw_submission_double(author=author, comments=[comment])


def praw_submission_continued_in_comments_double(n=0):
    author = praw_redditor()
    comment2 = praw_comment_double(author=author,
                                   body="long continuation 2" * 200,
                                   replies=[])
    comment1 = praw_comment_double(author=author,
                                   body="long continuation 1" * 200,
                                   replies=[comment2])
    comment_forest = praw.models.comment_forest.CommentForest(None, [comment1])
    return praw_submission_double(author=author, comments=comment_forest)


def praw_submission_with_ambiguous_next():
    return praw_submission_double(selftext="[next](link1) [next](link2)")


def praw_wikipage_double(_reddit, _subreddit, _pagename):
    return InstanceDouble("praw.models.reddit.wikipage.WikiPage",
                          content_md="[/r/hfy](http://www.reddit.com/r/HFY/)\n[some other link](http://redd.it/2oflhg)")


def story_double():
    return InstanceDouble("app.models.story.Story",
                          author_name="great author",
                          chapters=chapters_double(3),
                          date_start=1435000000.0,
                          date_end=1438000000,
                          title="great title",
                          id="555https%3A%2F%2Fwww.fanfiction.net%2Fs%2F10550829%2F1%2FGreat-Title")


praw_submissions = [
    praw_submission_double(0, title="some story", comments=praw_comments_double(3)),
    praw_submission_double(1, title="some story 02", comments=praw_comments_double(4)),
    praw_submission_double(2, title="some story 03", comments=praw_comments_double(5))
]
for subm in praw_submissions[0:-1]:
    # Add "Next" links to all but the last
    subm.selftext += f"[Next](https://www.reddit.com/r/great_subreddit/comments/00000{int(subm.id[-1:]) + 1}/great_title)"
praw_submissions[0].comments[2].body += "[some link](example.com)"


def find_praw_submission(_self=None, *, url=None, id=None):
    if url is not None:
        return [subm for subm in praw_submissions if subm.permalink == url][0]
    elif id is not None:
        return [subm for subm in praw_submissions if subm.id == id][0]
    raise
