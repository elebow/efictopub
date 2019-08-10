from app.models.story import Story

from tests.fixtures.doubles import chapter_double
from tests.fixtures.real import chapters_real


class TestStory:
    def setup_method(self):
        self.subject = Story(
            title="My Great Story",
            author="Great Author",
            summary="My Great Summary",
            chapters=chapters_real(3),
        )

    def test_date_start(self):
        self.subject.chapters = [
            chapter_double(date_published=5, date_updated=6),
            chapter_double(date_published=6, date_updated=7),
            chapter_double(date_published=7, date_updated=8),
        ]
        assert self.subject.date_start == 5

    def test_date_end(self):
        self.subject.chapters = [
            chapter_double(date_published=5, date_updated=6),
            chapter_double(date_published=6, date_updated=7),
            chapter_double(date_published=7, date_updated=8),
        ]
        assert self.subject.date_end == 8

    def test_id(self):
        assert self.subject.id == "start_date+0permalink+0"

    def test_as_dict(self):
        self.subject.chapters = [5, 5, 5]

        assert self.subject.as_dict() == {
            "title": "My Great Story",
            "author": "Great Author",
            "summary": "My Great Summary",
            "chapters": [5, 5, 5],
        }

    def test_from_dict(self):
        input_dict = {
            "title": "My Great Story",
            "author": "Great Author",
            "summary": "My Great Summary",
            "chapters": [5, 5, 5],
        }

        subject = Story.from_dict(input_dict)

        assert subject.title == "My Great Story"
        assert subject.author == "Great Author"
        assert subject.summary == "My Great Summary"
        assert subject.chapters == [5, 5, 5]
