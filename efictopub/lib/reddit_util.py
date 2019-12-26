import praw
import re

from efictopub import config
from efictopub.exceptions import AmbiguousIdError
from efictopub.models.reddit import RedditSubmission, RedditComment, RedditWikiPage


def redditor_name_from_url(url):
    matches = re.findall(r".*reddit.com/u/([^/?]*)", url)
    if matches:
        return matches[0]
    return None


def parse_id_or_url(thing, praw_reddit):
    if isinstance(thing, str):
        if len(thing) == 6:
            raise AmbiguousIdError
        # longer than 6 characters, assume it's a URL
        return parse_url(thing, praw_reddit)
    else:
        return None


def parse_url(url, praw_reddit):
    if re.match(r".*reddit.com/r/[^/]*?/comments/[^/]*?/[^/]*/?$", url):
        return RedditSubmission(praw.models.Submission(praw_reddit, url=url))

    if re.match(r".*reddit.com/r/[^/]*?/comments/[^/]*?/[^/]*/[^/]*/?$", url):
        return RedditComment(praw.models.Comment(praw_reddit, url=url))

    matches = re.findall(r".*reddit.com/r/(.*?)/wiki/(.*)$", url)[0]
    if matches:
        subreddit_name = matches[0]
        name = matches[1]
        subreddit = praw.models.Subreddit(praw_reddit, subreddit_name)
        return RedditWikiPage(praw.models.WikiPage(praw_reddit, subreddit, name))

    return None


def setup_reddit():
    return praw.Reddit(
        client_id=config.get(["reddit", "app"]),
        client_secret=config.get(["reddit", "secret"]),
        user_agent=config.get("user_agent"),
    )
