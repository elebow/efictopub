from unittest.mock import patch

from app import fetchers

from tests.fixtures.doubles import praw_wikipage_double


class TestFetchersRedditWikiPage:
    @patch("praw.models.WikiPage", praw_wikipage_double)
    def test_links_mentioned_in_wiki_page(self):
        links = fetchers.RedditWikiPage("reddit.com/r/whatever/wiki/whatever").links_mentioned_in_wiki_page()
        assert len(links) == 2
        assert links[0].href == "http://www.reddit.com/r/HFY/"
        assert links[-1].href == "http://redd.it/2oflhg"
