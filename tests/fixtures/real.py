# TODO rename this file to something like tests/support/fixtures.py

import pytest

import tests


def read_fixture(fname):
    with open(f"tests/fixtures/{fname}", "r") as file:
        return file.read()


ffnet_chapter_html_real = read_fixture("www.fanfiction.net_1.html")
ffnet_chapter_2_html_real = read_fixture("www.fanfiction.net_2.html")
ffnet_chapter_3_html_real = read_fixture("www.fanfiction.net_3.html")
ffnet_chapter_reviews_html_real = read_fixture("www.fanfiction.net_reviews.html")
ffnet_single_chapter_story_html_real = read_fixture("www.fanfiction.net_single.html")
ffnet_single_chapter_story_reviews_html_real = read_fixture(
    "www.fanfiction.net_single_reviews.html"
)

spacebattles_threadmarks_index_html = read_fixture(
    "spacebattles_threadmarks_index.html"
)
spacebattles_thread_reader_1_html = read_fixture("spacebattles_thread_reader_1.html")
spacebattles_thread_reader_2_html = read_fixture("spacebattles_thread_reader_2.html")

wordpress_chapter_html_real_1 = read_fixture("wordpress_1.html")
wordpress_chapter_html_real_2 = read_fixture("wordpress_2.html")


@pytest.fixture
def praw_comment(mocker):
    def praw_comment_without_replies():
        comment = mocker.Mock(
            author=mocker.Mock(),
            author_flair_text="Author Flair Text",
            body_html="body html",
            created_utc="5",
            edited="6",
            id="111111",
            permalink="permalink",
            replies=[],
            ups=5,
        )
        # `name` is a keyword argument of Mock, so set the attr separately
        comment.author.name = "Redditor Name"
        return comment

    comment = praw_comment_without_replies()
    comment.replies = [praw_comment_without_replies(), praw_comment_without_replies()]
    return comment


@pytest.fixture
def praw_submission(mocker, praw_comment):
    subm = mocker.MagicMock(
        author_name=mocker.MagicMock(),
        comments=mocker.MagicMock(),
        created_utc="5",
        edited="6",
        reddit_id="111111",
        permalink="permalink",
        selftext_html="selftext HTML",
        title="Submission Title",
        ups=5,
    )
    # `name` is a keyword argument of Mock, so set the attr separately
    subm.author.name = "Redditor Name"
    # comments should behave like a PRAW CommentForest. Or, an iterable MagicMock.
    subm.comments.__iter__.return_value = [praw_comment, praw_comment]
    return subm


@pytest.fixture
def redditor_with_submissions(mocker):
    mock_praw_submissions = [
        mocker.MagicMock(title="PRAW Submission 00", id="000000"),
        mocker.MagicMock(title="PRAW Submission 01", id="000001"),
        mocker.MagicMock(title="PRAW Submission 02", id="000002"),
    ]
    mock_redditor = mocker.MagicMock(
        submissions=mocker.MagicMock(
            new=mocker.Mock(return_value=mock_praw_submissions)
        )
    )
    return mock_redditor


def build_comment_forest():
    import praw
    from unittest.mock import MagicMock

    # CommentForest is bothersome to mock. Just use a real one.
    return praw.models.comment_forest.CommentForest(None, [MagicMock(), MagicMock()])


reddit_submissions = {
    "https://www.reddit.com/r/great_subreddit/comments/000000/next_links": lambda: tests.factories.RedditSubmissionFactory.build(
        selftext_html=f"<a href='https://www.reddit.com/r/great_subreddit/comments/000001/next_links'>Next</a>",
        permalink="https://www.reddit.com/r/great_subreddit/comments/000000/next_links",
    ),
    "https://www.reddit.com/r/great_subreddit/comments/000001/next_links": lambda: tests.factories.RedditSubmissionFactory.build(
        selftext_html=f"<a href='https://www.reddit.com/r/great_subreddit/comments/000002/next_links'>Next</a>",
        permalink="https://www.reddit.com/r/great_subreddit/comments/000001/next_links",
    ),
    "https://www.reddit.com/r/great_subreddit/comments/000002/next_links": lambda: tests.factories.RedditSubmissionFactory.build(
        selftext_html=f"<a href='https://www.reddit.com/r/great_subreddit/comments/555/some_other_page'>Some other page</a>",
        permalink="https://www.reddit.com/r/great_subreddit/comments/000002/next_links",
    ),
    "https://www.reddit.com/r/great_subreddit/comments/000003/ambiguous_next": lambda: tests.factories.RedditSubmissionFactory.build(
        selftext_html="<a href='link1'>next</a> <a href='link2'>next</a>"
    ),
    "https://www.reddit.com/r/great_subreddit/comments/000004/duplicate_next": lambda: tests.factories.RedditSubmissionFactory.build(
        # point it to 000002/next_links, which is a dead end
        selftext_html="""
        <a href='https://www.reddit.com/r/great_subreddit/comments/000002/next_links'>next</a>
        <a href='https://www.reddit.com/r/great_subreddit/comments/000002/next_links'>next</a>
    """
    ),
    "https://www.reddit.com/r/great_subreddit/comments/000005/has_comments": lambda: tests.factories.RedditSubmissionFactory.build(
        comments=build_comment_forest()
    ),
}


def get_reddit_submission(url, _praw_reddit=None):
    return reddit_submissions[url]()
