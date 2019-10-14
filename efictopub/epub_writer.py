from datetime import datetime
import mkepub
import os
import pathlib

from efictopub import config


class EpubWriter:
    def __init__(self, story):
        self.story = story
        self.book = mkepub.Book(
            title=self.story.title,
            author=self.story.author,
            published=datetime.utcfromtimestamp(
                self.story.date_end  # dc:date
            ).isoformat(),
            dcterms={
                "available": datetime.utcfromtimestamp(
                    self.story.date_start  # dcterms:modified
                ).isoformat()
            },
        )

    def write_epub(self):
        self.add_cover()
        self.add_info_page()
        self.add_chapters()

        output_filename = self.output_filename()
        self.book.save(output_filename)
        print(f"wrote {output_filename}")

    def add_chapters(self):
        for chapter in self.story.chapters:
            # TODO use add_chapter if https://github.com/anqxyr/mkepub/pull/13 is merged
            self.book.add_page(chapter.title, self.text_for_chapter(chapter))

    def add_cover(self):
        # self.book.set_cover(self.story.cover_svg)
        # TODO imghdr doesn't recognize SVG, and mkepub doesn't allow manually-specified extensions
        # replicate the effects with private methods here until an upstream PR is accepted
        cover_svg = bytes(self.story.cover_svg, "utf-8")
        self.book._cover = "cover.svg"
        self.book._add_file(pathlib.Path("covers") / self.book._cover, cover_svg)
        self.book._write("cover.xhtml", "EPUB/cover.xhtml", cover=self.book._cover)

    def add_info_page(self):
        self.book.add_page("info", f"{self.story.title}<br>by {self.story.author}")

    def text_for_chapter(self, chapter):
        if len(self.story.chapters) > 1:
            return f"{chapter.title}\n\n{chapter.text}"
        else:
            return chapter.text

    def output_filename(self):
        return config.get("outfile") or os.path.join(
            config.get("epub_location"), self.story.filename
        )
