from datetime import datetime
import random

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
    date_published = factory.Sequence(lambda n: f"published date {n}")
    date_updated = factory.Sequence(lambda n: f"updated date {n}")
    permalink = factory.Sequence(lambda n: f"permalink {n}")
    score = factory.Sequence(lambda n: f"score {n}")
    text = factory.Sequence(lambda n: f"text {n}")

    @factory.LazyAttribute
    def replies(self):
        if self.tree_depth <= 0:
            return []
        else:
            num_children = random.randint(0, 3)
            return [
                CommentFactory.build(tree_depth=self.tree_depth - 1)
                for m in range(num_children)
            ]


class StoryFactory(factory.Factory):
    class Meta:
        model = efictopub.models.story.Story

    author = factory.Sequence(lambda n: f"Story Author Name {n}")
    chapters = factory.List([factory.SubFactory(ChapterFactory) for n in range(3)])
    date_fetched = 1553317565
    title = factory.Sequence(lambda n: f"Great Story Title {n}")
