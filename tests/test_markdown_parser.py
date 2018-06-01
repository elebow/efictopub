from app.markdown_parser import MarkdownParser


class TestMarkdownParser:
    def setup_method(self):
        self.src = """
            here is some markdown
            [Prev](example.com/first)
            [click here for next, with a title](example.com/second "title goes here")
            (malformed link 1)[example.com]
            [malformed link 2] (example.com)
            [snexto](example.com/not_next)

        """
        self.parser = MarkdownParser(self.src)

    def test_parse_links(self):
        assert(len(self.parser.links) == 3)

        assert(self.parser.links[0].href == "example.com/first")
        assert(self.parser.links[0].text == "Prev")

        assert(self.parser.links[1].href == "example.com/second")
        assert(self.parser.links[1].text == "click here for next, with a title")
        assert(self.parser.links[1].title == "title goes here")

    def test_links_containing_text(self):
        next_links = self.parser.links_containing_text("next")
        assert(len(next_links) == 1)
        assert(next_links[0].text == "click here for next, with a title")

        prev_links = self.parser.links_containing_text("prev")
        assert(len(prev_links) == 1)
        assert(prev_links[0].text == "Prev")
