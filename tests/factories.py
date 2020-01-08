import efictopub.models.chapter
import efictopub.models.comment
import efictopub.models.story

import factory


class ChapterFactory(factory.Factory):
    class Meta:
        model = efictopub.models.chapter.Chapter

    comments = factory.List(
        [
            factory.SubFactory("tests.factories.CommentFactory", tree_depth=3)
            for n in range(3)
        ]
    )
    date_published = factory.Sequence(lambda n: 100 * n)
    date_updated = factory.Sequence(lambda n: 100 * n + 50)
    permalink = factory.Sequence(lambda n: f"permalink {n}")
    score = 5
    text = factory.Sequence(lambda n: f"<p>chapter content {n}</p>")
    title = factory.Sequence(lambda n: f"Chapter Title {n}")


class CommentFactory(factory.Factory):
    class Meta:
        model = efictopub.models.comment.Comment
        exclude = ("tree_depth",)

    author = factory.Sequence(lambda n: f"Comment Author Name {n}")
    date_published = factory.Sequence(lambda n: 10000 * n)
    date_updated = factory.Sequence(lambda n: 10000 * n + 100)
    permalink = factory.Sequence(lambda n: f"permalink {n}")
    score = factory.Sequence(lambda n: f"score {n}")
    text = factory.Sequence(lambda n: f"text {n}")

    @factory.LazyAttribute
    def replies(self):
        if self.tree_depth <= 0:
            return []
        else:
            num_children = self.tree_depth - 1
            return [
                CommentFactory.build(tree_depth=self.tree_depth - 1)
                for m in range(num_children)
            ]


class StoryFactory(factory.Factory):
    class Meta:
        model = efictopub.models.story.Story
        exclude = ("num_chapters",)

    author = factory.Sequence(lambda n: f"Story Author Name {n}")
    chapters = factory.LazyAttribute(
        lambda o: [ChapterFactory.build() for n in range(o.num_chapters)]
    )
    date_fetched = 1553317565
    title = factory.Sequence(lambda n: f"Great Story Title {n}")

    num_chapters = 1


class RedditSubmissionFactory(factory.Factory):
    class Meta:
        model = efictopub.models.reddit.reddit_submission.RedditSubmission

    @classmethod
    def _adjust_kwargs(cls, **kwargs):
        # RedditSubmission only takes a PRAW submission object. PRAW objects are too annoying to build.
        # So, just pass in a Mock that behaves like a PRAW submission obj.
        from unittest.mock import MagicMock

        praw_subm_attrs = {
            "author": MagicMock(name="Submission Author Name {n}"),
            "author_flair_text": "Author Flair Text",
            "comments": MagicMock(),
            "created_utc": "published date {n}",
            "edited": "updated date {n}",
            "id": "reddit_id_{n}",
            "permalink": "permalink {n}",
            "selftext_html": "<p>chapter content {n}</p>",
            "title": "Chapter Title {n}",
            "ups": factory.Sequence(lambda n: f"upvotes_{n}"),
        }
        praw_subm_attrs.update(kwargs)
        mock_praw_subm = MagicMock("praw.models.Submission", **praw_subm_attrs)
        return {"praw_submission": mock_praw_subm}
