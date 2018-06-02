import pytest
from unittest.mock import MagicMock

from app.models.story import Story


@pytest.fixture()
def chapters():
    return [
        MagicMock("Chapter", get_text=lambda: "chapter 1", created_utc="start_date", permalink="permalink",
                  author_name="great-author", title="great-title"),
        MagicMock("Chapter", get_text=lambda: "chapter 2"),
        MagicMock("Chapter", get_text=lambda: "chapter 3", created_utc="end_date")
    ]


class TestStory:

    def setup_method(self):
        self.subject = Story(chapters=chapters())

    def test_calculate_id(self):
        assert self.subject.id == "start_datepermalink"

    def test_calculate_title(self):
        assert self.subject.title == "great-title"
