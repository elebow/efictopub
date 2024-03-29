import efictopub.fetchers


class TestFetchers__init__:
    def test_fetcher_for_url(self):
        assert (
            efictopub.fetchers.fetcher_for_url(
                "https://www.fanfiction.net/s/555/1/My-Great-Story"
            ).__module__
            == "efictopub.fetchers.ffnet"
        )

        assert (
            efictopub.fetchers.fetcher_for_url(
                "https://archiveofourown.org/works/55555555"
            ).__module__
            == "efictopub.fetchers.ao3"
        )

        assert (
            efictopub.fetchers.fetcher_for_url(
                "https://www.reddit.com/u/redditor"
            ).__module__
            == "efictopub.fetchers.reddit_author"
        )

        assert (
            efictopub.fetchers.fetcher_for_url(
                "https://www.reddit.com/r/subreddit/comments/555/whatever"
            ).__module__
            == "efictopub.fetchers.reddit_next"
        )

        assert (
            efictopub.fetchers.fetcher_for_url(
                "https://www.reddit.com/r/subreddit/wiki/whatever"
            ).__module__
            == "efictopub.fetchers.reddit_wiki_page"
        )

        assert (
            efictopub.fetchers.fetcher_for_url(
                "https://blog-name.wordpress.com/2011/06/11/1-1/"
            ).__module__
            == "efictopub.fetchers.wordpress"
        )

        assert (
            efictopub.fetchers.fetcher_for_url(
                "README.md"  # an existing file
            ).__module__
            == "efictopub.fetchers.archive"
        )
