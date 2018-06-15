from app.models.story import Story

from tests.fixtures.real import chapters_real


class TestStory:

    def setup_method(self):
        chapters = chapters_real(3)
        self.subject = Story(chapters=chapters)

    def test_calculate_id(self):
        assert self.subject.id == "start_date+0permalink+0"

    def test_calculate_title(self):
        assert self.subject.title == "great-title 0"
