class Comment:
    def __init__(self, praw_comment):
        self.author_name = praw_comment.author.name if praw_comment.author else "[n/a]"
        self.author_flair_text = praw_comment.author_flair_text
        self.body = praw_comment.body
        self.created_utc = praw_comment.created_utc
        self.edited = praw_comment.edited
        self.reddit_id = praw_comment.id
        self.replies = self.replies_for_comment(praw_comment)
        self.permalink = praw_comment.permalink
        self.ups = praw_comment.ups

    def replies_for_comment(self, praw_comment):
        return [Comment(c) for c in praw_comment.replies]
