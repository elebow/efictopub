import pytest

from efictopub.fetchers import reddit_wiki_page


@pytest.fixture
def praw_wikipage(mocker):
    return mocker.Mock(
        return_value=mocker.Mock(
            content_html="<a href='http://www.reddit.com/r/HFY/'>/r/hfy</a>)\n<a href='http://redd.it/2oflhg'>some other link</a>"
        )
    )


class TestFetchersRedditWikiPage:
    def test_links_mentioned_in_wiki_page(self, mocker, praw_wikipage):
        mocker.patch("praw.models.WikiPage", praw_wikipage)
        links = reddit_wiki_page.Fetcher(
            "reddit.com/r/whatever/wiki/whatever"
        ).links_mentioned_in_wiki_page()
        assert len(links) == 2
        assert links[0].href == "http://www.reddit.com/r/HFY/"
        assert links[-1].href == "http://redd.it/2oflhg"
