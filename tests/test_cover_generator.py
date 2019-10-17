import re

from efictopub.cover_generator import CoverGenerator


class TestCoverGenerator:
    def test_generate_cover_svg(self, story_factory):
        story = story_factory.build()
        generator = CoverGenerator(story)
        svg = generator.generate_cover_svg()

        assert re.search(fr"<text[^>]*?>{story.title}</text>", svg) is not None
        assert "1969-12-31 – 1969-12-31 (fetched 2019-03-23)" in svg
        assert re.search(fr"<text[^>]*?>{story.author}</text>", svg) is not None
        assert (
            re.search(fr"<text[^>]*?>{story.chapters[0].permalink}</text>", svg)
            is not None
        )
