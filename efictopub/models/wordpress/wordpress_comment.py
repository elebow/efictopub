class WordpressComment:
    def __init__(self, comment_element):
        self.comment_elem = comment_element.find("article")

        all_children_elems = comment_element.select(".children")

        if all_children_elems:
            # select(".children") will also find grandchildren, so only take the [0] element
            self.children_elems = all_children_elems[0].select("li.comment")
        else:
            self.children_elems = []

    @property
    def author(self):
        return self.comment_elem.select(".comment-author .fn")[0].text

    @property
    def text(self):
        return (
            self.comment_elem.select(".comment-content")[0]
            .encode_contents()
            .decode()
            .strip()
        )

    @property
    def replies(self):
        return [WordpressComment(reply) for reply in self.children_elems]
