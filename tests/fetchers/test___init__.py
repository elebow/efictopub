import app.fetchers


class TestFetchers__init__:
    def test_fetcher_for_url(self):
        assert app.fetchers.fetcher_for_url("https://www.fanfiction.net/s/555/1/My-Great-Story").__class__.__name__ \
            == "FFNet"

        assert app.fetchers.fetcher_for_url("https://www.reddit.com/u/redditor").__class__.__name__ \
            == "RedditAuthor"

        assert app.fetchers.fetcher_for_url("https://www.reddit.com/r/subreddit/comments/555/whatever").__class__.__name__ \
            == "RedditNext"

        assert app.fetchers.fetcher_for_url("https://www.reddit.com/r/subreddit/wiki/whatever").__class__.__name__ \
            == "RedditWikiPage"
