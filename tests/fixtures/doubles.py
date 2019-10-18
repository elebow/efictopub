import praw

from doubles import InstanceDouble


def praw_wikipage_double(_reddit, _subreddit, _pagename):
    return InstanceDouble(
        "praw.models.reddit.wikipage.WikiPage",
        content_html="<a href='http://www.reddit.com/r/HFY/'>/r/hfy</a>)\n<a href='http://redd.it/2oflhg'>some other link</a>",
    )
