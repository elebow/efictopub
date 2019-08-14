from efictopub.html_parser import HTMLParser


class TestHTMLParser:
    def setup_method(self):
        self.src = """
here is some html
<a href="example.com/first">Prev</a>
<a href="example.com/second" title="title goes here">click here for next, with a title</a>
<a href="example.com/third">link with <em>formatting</em> in it</a>
<a href="example.com/not_next">snexto</a>

"""
        self.parser = HTMLParser(self.src)

    def test_parse_links(self):
        assert len(self.parser.links) == 4

        assert self.parser.links[0].href == "example.com/first"
        assert self.parser.links[0].text == "Prev"

        assert self.parser.links[1].href == "example.com/second"
        assert self.parser.links[1].text == "click here for next, with a title"
        assert self.parser.links[1].title == "title goes here"

        assert self.parser.links[2].text == "link with formatting in it"

    def test_links_containing_text(self):
        next_links = self.parser.links_containing_text("next")
        assert len(next_links) == 1
        assert next_links[0].text == "click here for next, with a title"

        prev_links = self.parser.links_containing_text("prev")
        assert len(prev_links) == 1
        assert prev_links[0].text == "Prev"
