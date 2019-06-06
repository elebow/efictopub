import app.fetchers


class TestFetchers__init__:
    def test_fetcher_for_url(self):
        assert (
            app.fetchers.fetcher_for_url("https://www.fanfiction.net/s/555/1/My-Great-Story").__module__
            == "ffnet"
        )

        assert app.fetchers.fetcher_for_url("https://www.reddit.com/u/redditor").__module__ == "reddit_author"

        assert (
            app.fetchers.fetcher_for_url(
                "https://www.reddit.com/r/subreddit/comments/555/whatever"
            ).__module__
            == "reddit_next"
        )

        assert (
            app.fetchers.fetcher_for_url("https://www.reddit.com/r/subreddit/wiki/whatever").__module__
            == "reddit_wiki_page"
        )
