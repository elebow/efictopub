import re

from app.cover_generator import CoverGenerator

from tests.fixtures.doubles import story_double


class TestCoverGenerator:
    def test_generate_cover_svg(self):
        story = story_double()
        generator = CoverGenerator(story)
        svg = generator.generate_cover_svg()

        assert re.search(fr"<text[^>]*?>{story.title}</text>", svg) is not None
        assert "2015-06-22 – 2015-07-27 (fetched 2019-03-23)" in svg
        assert re.search(fr"<text[^>]*?>{story.author}</text>", svg) is not None
        assert (
            re.search(fr"<text[^>]*?>{story.chapters[0].permalink}</text>", svg)
            is not None
        )
