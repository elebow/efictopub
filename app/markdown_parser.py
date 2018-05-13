import re

from collections import namedtuple


class MarkdownParser:
    # This regexp-based parser fails to account for the markdown syntax that allows
    # links to be defined first and the href supplied later in the document.
    LINK_REGEXP = re.compile(r'\[(.*?)\]\((.*?)(?: "(.*)")?\)', re.IGNORECASE)

    Link = namedtuple("Link", ["href", "text", "title"])

    def __init__(self, src):
        self.src = src

        self.parse_links()

    # Return all the links contaning a specified string.
    # This is useful for finding prev/next links in a post that is part of a series.
    # Note that link text is already downcased in parse_links().
    def links_containing_text(self, text_to_find):
        regexp_to_find = re.compile(r"\b%s\b" % text_to_find, re.IGNORECASE)
        return [link for link in self.links if regexp_to_find.search(link.text)]

    def parse_links(self):
        self.links = [
            self.Link(href=link[1], text=link[0], title=link[2])
            for link
            in self.LINK_REGEXP.findall(self.src)
        ]
