from efictopub.html_parser import HTMLParser

import pytest


class TestHTMLParser:
    @pytest.fixture
    def parser(self):
        src = """
here is some html
<a href="example.com/first">Prev</a>
<a href="example.com/second" title="title goes here">click here for next, with a title</a>
<a href="example.com/third">link with <em>formatting</em> in it</a>
<a href="example.com/not_next">snexto</a>
<a href="example.com/second" rel="next">Forward</a>

"""
        return HTMLParser(src)

    def test_parse_links(self, parser):
        assert len(parser.a_elements) == 5

        assert parser.a_elements[0].attrs["href"] == "example.com/first"
        assert parser.a_elements[0].text == "Prev"

        assert parser.a_elements[1].attrs["href"] == "example.com/second"
        assert parser.a_elements[1].text == "click here for next, with a title"
        assert parser.a_elements[1].attrs["title"] == "title goes here"

        assert parser.a_elements[2].text == "link with formatting in it"

    def test_links_containing_text(self, parser):
        next_links = parser.links_containing_text("next")
        assert len(next_links) == 1
        assert next_links[0].text == "click here for next, with a title"

        prev_links = parser.links_containing_text("prev")
        assert len(prev_links) == 1
        assert prev_links[0].text == "Prev"
