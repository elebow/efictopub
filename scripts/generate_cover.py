#!/usr/bin/python3

# PYTHONPATH=../efictopub ./scripts/generate_cover.py cover.svg

import sys

import efictopub
from efictopub.models.chapter import Chapter
from efictopub.models.story import Story

efictopub.config.load({}, fetcher=None)

chapters = [
    Chapter(
        comments=[],
        date_published=5,
        date_updated=6,
        permalink="http://example.com/story5",
        score=7,
        text="chapter text",
        title="chapter title",
    )
]
story = Story(
    title="My Great Story with a very long title that will span several lines",
    author="Author Name",
    chapters=chapters,
)
svg = story.cover_svg

with open(sys.argv[1], "w") as outfile:
    outfile.write(svg)
