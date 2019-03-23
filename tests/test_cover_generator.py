import re

from app.cover_generator import CoverGenerator

from tests.fixtures.doubles import story_double


class TestCoverGenerator:
    def test_generate_cover_svg(self):
        story = story_double()
        generator = CoverGenerator(story)
        svg = generator.generate_cover_svg()

        assert re.search(r"<text.*?>%s</text>" % story.title, svg) is not None
        assert "2015-06-22 – 2015-07-27 (fetched TODO)" in svg
