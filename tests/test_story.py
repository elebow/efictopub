from app.models.story import Story

from tests.fixtures.doubles import chapter_double
from tests.fixtures.real import chapters_real


class TestStory:

    def setup_method(self):
        chapters = chapters_real(3)
        self.subject = Story(chapters=chapters)

    def test_date_start(self):
        self.subject.chapters = [chapter_double(date_published=5, date_updated=6),
                                 chapter_double(date_published=6, date_updated=7),
                                 chapter_double(date_published=7, date_updated=8)]
        assert self.subject.date_start == 5

    def test_date_end(self):
        self.subject.chapters = [chapter_double(date_published=5, date_updated=6),
                                 chapter_double(date_published=6, date_updated=7),
                                 chapter_double(date_published=7, date_updated=8)]
        assert self.subject.date_end == 8

    def test_id(self):
        assert self.subject.id == "start_date+0permalink+0"

    def test_title(self):
        assert self.subject.title == "My Great Story"
