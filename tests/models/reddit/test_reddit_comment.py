from efictopub.models.reddit import RedditComment


class TestRedditComment:
    def test_as_comment(self, praw_comment):
        reddit_comment = RedditComment(praw_comment)
        comment = reddit_comment.as_comment()

        assert comment.author == "Redditor Name (Author Flair Text)"
        assert comment.date_published == "5"
        assert comment.date_updated == "6"
        assert len(comment.replies) == 2
