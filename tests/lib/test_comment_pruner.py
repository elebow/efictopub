from efictopub.lib import comment_pruner
from efictopub.models.comment import Comment


def build_comment(author, replies):
    if not replies:
        new_replies = []
    else:
        new_replies = [
            build_comment(author, replies) for author, replies in replies.items()
        ]
    return Comment(
        author=author,
        date_published=None,
        date_updated=None,
        permalink=None,
        replies=new_replies,
        score=None,
        text=None,
    )


def extract_authors(comment):
    if not comment.replies:
        return {comment.author: {}}
    return {comment.author: extract_authors(reply) for reply in comment.replies}


class TestCommentPruner:
    def test_tree_contains_author(self):
        tree = build_comment("hhh", {})
        assert comment_pruner.tree_contains_author(tree, "hhh") is True

        tree = build_comment("hhh", {})
        assert comment_pruner.tree_contains_author(tree, "author9") is False

        tree = build_comment("author1", {"hhh": []})
        assert comment_pruner.tree_contains_author(tree, "hhh") is True

        tree = build_comment("author1", {"hhh": {"author3": {}}, "author5": {}})
        assert comment_pruner.tree_contains_author(tree, "hhh") is True

    def test_tree_containing_author(self):
        root = build_comment(
            "author0", {"author1": {"hhh": {"author3": {}}}, "author4": {}}
        )

        assert extract_authors(comment_pruner.tree_containing_author(root, "hhh")) == {
            "author0": {"author1": {"hhh": {}}}
        }

        root = build_comment(
            "author0",
            {
                "author1": {"author5": {"author6": {}, "hhh": {"author3": {}}}},
                "author4": {},
            },
        )

        assert extract_authors(comment_pruner.tree_containing_author(root, "hhh")) == {
            "author0": {"author1": {"author5": {"hhh": {}}}}
        }
