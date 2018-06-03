import praw
import re

from app import config
from app.exceptions import AmbiguousIdError
from app.models import reddit


def parse_thing_or_id_or_url(thing):
    if isinstance(thing, praw.models.reddit.submission.Submission):
        return reddit.Submission(thing)
    elif isinstance(thing, praw.models.reddit.comment.Comment):
        return reddit.Comment(thing)
    elif isinstance(thing, praw.models.WikiPage):
        return None #WikiPage(thing) #TODO
    elif isinstance(thing, str):
        if len(thing) == 6:
            raise AmbiguousIdError
        # longer than 6 characters, assume it's a URL
        return parse_url(thing)


def parse_url(url, *, praw_reddit):
    if re.match(r'.*reddit.com/r/[^/]*?/comments/[^/]*?/[^/]*/?$', url):
        return reddit.Submission(praw.models.Submission(praw_reddit, url=url))

    if re.match(r'.*reddit.com/r/[^/]*?/comments/[^/]*?/[^/]*/[^/]*/?$', url):
        return reddit.Comment(praw.models.Comment(praw_reddit, url=url))

    return None #TODO
    matches = re.findall(r'.*reddit.com/r/(.*?)/wiki/(.*)$', url)[0]
    if matches:
        subreddit = matches[0]
        name = matches[1]
        return reddit.WikiPage(praw.models.WikiPage(praw_reddit, subreddit, name))

    return None


def setup_reddit():
    return praw.Reddit(client_id=config.reddit.app,
                       client_secret=config.reddit.secret,
                       user_agent=config.reddit.user_agent)
