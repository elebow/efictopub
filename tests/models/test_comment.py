from efictopub.models.comment import Comment


class TestComment:
    def test_as_html(self, comment_factory):
        # We can't build the comment tree with the recursive factory, because we want
        # control over the values of every comment so we can assert the full output.
        comment_factory.reset_sequence()
        comment = comment_factory.build(text="Comment 1", tree_depth=0)
        comment.replies = [
            comment_factory.build(text="Comment 2", tree_depth=0),
            comment_factory.build(text="Comment 3", tree_depth=0),
        ]
        comment.replies[0].replies = [
            comment_factory.build(text="Comment 4", tree_depth=0),
            comment_factory.build(text="Comment 5", tree_depth=0),
        ]
        html = comment.as_html()

        assert (
            html
            == "<div class='comment'>"
            + "<div class='comment-author'>Comment Author Name 0 (1970-01-01, edited 1970-01-01)</div>"
            + "<p>Comment 1</p>"
            + "<div class='replies'>"
            + "<div class='comment'>"
            + "<div class='comment-author'>Comment Author Name 1 (1970-01-01, edited 1970-01-01)</div>"
            + "<p>Comment 2</p>"
            + "<div class='replies'>"
            + "<div class='comment'><div class='comment-author'>Comment Author Name 3 (1970-01-01, edited 1970-01-01)</div><p>Comment 4</p></div>"
            + "<div class='comment'><div class='comment-author'>Comment Author Name 4 (1970-01-01, edited 1970-01-01)</div><p>Comment 5</p></div>"
            + "</div>"
            + "</div>"
            + "<div class='comment'><div class='comment-author'>Comment Author Name 2 (1970-01-01, edited 1970-01-01)</div><p>Comment 3</p></div>"
            + "</div>"
            + "</div>"
        )
