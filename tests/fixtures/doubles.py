import praw

from doubles import InstanceDouble


def praw_redditor(n=0):
    return InstanceDouble("praw.models.Redditor", name=f"redditor {n}")


def praw_redditor_with_submissions_double(name="some redditor"):
    return InstanceDouble(
        "praw.models.Redditor",
        name=name,
        submissions=InstanceDouble(
            "praw.models.listing.mixins.redditor.SubListing",
            new=lambda: praw_submissions,
        ),
    )


def praw_comment_double(
    n=0,
    author=praw_redditor(),
    body_html='<div class="md"><p>some body text</p>\n</div>',
    replies=[],
):
    return InstanceDouble(
        "praw.models.reddit.comment.Comment",
        author=author,
        author_flair_text="",
        body_html=body_html,
        created_utc=f"created utc {n}",
        edited=f"edited timestamp {n}",
        id="reddit id {n}",
        permalink=f"permalink {n}",
        replies=replies,
        ups=5,
    )


def praw_comments_double(count):
    return [praw_comment_double(n) for n in range(0, count)]


def praw_submission_double(
    n=0,
    author=-1,
    comments=[],
    selftext_html='<!-- SC_OFF --><div class="md"><p>some selftext_html</p>\n\n<p>second line</p>\n</div><!-- SC_ON -->',
    title="some title",
):
    author = praw_redditor(n) if author == -1 else author
    # CommentForest is bothersome to mock. It needs to be iterable.
    comment_forest = praw.models.comment_forest.CommentForest(None, comments)
    return InstanceDouble(
        "praw.models.reddit.submission.Submission",
        author=author,
        comments=comment_forest,
        created_utc=f"created utc {n}",
        edited=f"edited timestamp {n}",
        id=f"00000{n}",
        permalink=f"https://www.reddit.com/r/great_subreddit/comments/00000{n}/great_title",
        selftext_html=selftext_html,
        title=title,
        ups=5,
    )


def praw_submissions_double(count):
    return [praw_submission_double(n) for n in range(0, count)]


def praw_submission_with_author_note_double(n=0):
    author = praw_redditor()
    comment = praw_comment_double(author=author, body_html="short author note")
    return praw_submission_double(author=author, comments=[comment])


def praw_submission_continued_in_comments_double(n=0):
    author = praw_redditor()
    comment2 = praw_comment_double(
        author=author, body_html="long continuation 2" * 200, replies=[]
    )
    comment1 = praw_comment_double(
        author=author, body_html="long continuation 1" * 200, replies=[comment2]
    )
    comment_forest = praw.models.comment_forest.CommentForest(None, [comment1])
    return praw_submission_double(author=author, comments=comment_forest)


def praw_submission_with_ambiguous_next():
    return praw_submission_double(
        selftext_html="<a href='link1'>next</a> <a href='link2'>next</a>"
    )


def praw_submission_with_duplicate_next():
    return praw_submission_double(
        selftext_html="""
        <a href='https://www.reddit.com/r/great_subreddit/comments/000000/great_title'>next</a>
        <a href='https://www.reddit.com/r/great_subreddit/comments/000000/great_title'>next</a>
    """
    )


def praw_wikipage_double(_reddit, _subreddit, _pagename):
    return InstanceDouble(
        "praw.models.reddit.wikipage.WikiPage",
        content_html="<a href='http://www.reddit.com/r/HFY/'>/r/hfy</a>)\n<a href='http://redd.it/2oflhg'>some other link</a>",
    )


praw_submissions = [
    praw_submission_double(0, title="some story", comments=praw_comments_double(3)),
    praw_submission_double(1, title="some story 02", comments=praw_comments_double(4)),
    praw_submission_double(2, title="some story 03", comments=praw_comments_double(5)),
]
for subm in praw_submissions[0:-1]:
    # Add "Next" links to all but the last
    subm.selftext_html += f"<a href='https://www.reddit.com/r/great_subreddit/comments/00000{int(subm.id[-1:]) + 1}/great_title'>Next</a>"
praw_submissions[0].comments[2].body_html += "<a href='example.com'>some link</a>"


def find_praw_submission(_self=None, *, url=None, id=None):
    if url is not None:
        return [subm for subm in praw_submissions if subm.permalink == url][0]
    elif id is not None:
        return [subm for subm in praw_submissions if subm.id == id][0]
    raise
