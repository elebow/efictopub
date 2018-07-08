class WikiPage:
    def __init__(self, praw_wikipage):
        self.praw_wikipage = praw_wikipage
        self.text = praw_wikipage.content_md
