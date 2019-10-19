import copy


def tree_contains_author(root, author_name):
    if getattr(root, "_tree_contains_author", None):
        return root._tree_contains_author
    elif not root.replies:
        return root.author == author_name
    else:
        found_in_replies = root.author == author_name or any(
            [tree_contains_author(reply, author_name) for reply in root.replies]
        )
        root._tree_contains_author = found_in_replies
        return found_in_replies


def tree_containing_author(root, author_name):
    """Prune any comment other than by the specified author or ancestors thereof"""
    if not root.replies:
        # leaf node
        if root.author == author_name:
            return copy.copy(root)
        else:
            return None
    else:
        # non-leaf node
        new_replies = [
            tree_containing_author(reply, author_name) for reply in root.replies
        ]
        new_replies = list(filter(None, new_replies))

        if not new_replies:
            # none of the children contain an author comment...
            if root.author == author_name:
                # ...but root is an author comment
                new_root = copy.copy(root)
                new_root.replies = []  # none of the replies matched, so omit them
                return new_root
            else:
                # ...but root is an author comment
                return None
        else:
            # at least one child contains an author comment
            new_root = copy.copy(root)
            new_root.replies = new_replies
            return new_root
