from datetime import datetime

from freezegun import freeze_time

from efictopub.models.story import Story


def build_three_chapters(chapter_factory):
    return [
        chapter_factory.build(
            date_published=5, date_updated=6, permalink="permalink for chapter 0"
        ),
        chapter_factory.build(date_published=6, date_updated=7),
        chapter_factory.build(date_published=7, date_updated=8),
    ]


class TestStory:
    def test_date_start(self, chapter_factory):
        subject = Story(chapters=build_three_chapters(chapter_factory))

        assert subject.date_start == 5

    def test_date_end(self, chapter_factory):
        subject = Story(chapters=build_three_chapters(chapter_factory))

        assert subject.date_end == 8

    def test_id(self, chapter_factory):
        chapters = build_three_chapters(chapter_factory)
        subject = Story(chapters=chapters)

        assert subject.id == "5permalink+for+chapter+0"

    @freeze_time("2000-01-01")
    def test_as_dict(self):
        subject = Story(
            title="My Great Story",
            author="Great Author",
            summary="My Great Summary",
            chapters=[5, 5, 5],
        )

        assert subject.as_dict() == {
            "title": "My Great Story",
            "author": "Great Author",
            "summary": "My Great Summary",
            "chapters": [5, 5, 5],
            "date_fetched": datetime(2000, 1, 1).timestamp(),
        }

    def test_from_dict(self):
        input_dict = {
            "title": "My Great Story",
            "author": "Great Author",
            "summary": "My Great Summary",
            "chapters": [5, 5, 5],
            "date_fetched": "today!",
        }

        subject = Story.from_dict(input_dict)

        assert subject.title == "My Great Story"
        assert subject.author == "Great Author"
        assert subject.summary == "My Great Summary"
        assert subject.chapters == [5, 5, 5]
        assert subject.date_fetched == "today!"
