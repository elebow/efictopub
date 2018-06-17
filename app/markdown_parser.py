from collections import namedtuple
import mistletoe
from mistletoe import ast_renderer, html_renderer
import re


class MarkdownParser:
    Link = namedtuple("Link", ["href", "text", "title"])

    def __init__(self, src):
        self.mt_document = mistletoe.Document(src + "\n")
        self.tree = ast_renderer.get_ast(self.mt_document)
        self.links = [self.build_link(link) for link in self.generate_nodes(self.tree, node_type="Link")]

    def as_html(self):
        renderer = html_renderer.HTMLRenderer()
        return renderer.render(self.mt_document)

    # Return all the links contaning a specified string.
    # This is useful for finding prev/next links in a post that is part of a series.
    # Note that link text is already downcased in parse_links().
    def links_containing_text(self, text_to_find):
        regexp_to_find = re.compile(r"\b%s\b" % text_to_find, re.IGNORECASE)
        return [link for link in self.links if regexp_to_find.search(link.text)]

    def generate_nodes(self, node, *, node_type):
        if node["type"] == node_type:
            yield node

        if "children" in node.keys():
            for child in node["children"]:
                for link in self.generate_nodes(child, node_type=node_type):
                    yield link

    def build_link(self, link_dict):
        return self.Link(href=link_dict["target"],
                         text="".join([text["content"]
                                       for text
                                       in self.generate_nodes(link_dict, node_type="RawText")]),
                         title=link_dict["title"])
