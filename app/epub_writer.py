from datetime import datetime
from ebooklib import epub
import functools


class EpubWriter:
    def __init__(self, story, outfile_name):
        self.story = story
        self.book = epub.EpubBook()
        self.outfile_name = outfile_name

    def write_epub(self):
        self.book.set_title(self.story.title)
        self.book.set_language("en")

        self.book.add_author(self.story.author_name)

        # dc:date MUST be the time the EPUB file was generated
        self.book.add_metadata("DC", "date", datetime.utcnow().isoformat())

        # dcterms:modified is the last-modified date of the book content
        epub_options = {"mtime": datetime.utcfromtimestamp(self.story.date_end)}

        # dcterms:available is defined here to be the date the first chapter was published
        self.book.add_metadata(
            None,
            "meta",
            datetime.utcfromtimestamp(self.story.date_start).isoformat(),
            {"property": "dcterms:available"},
        )

        self.add_cover()
        self.add_info_page()
        self.add_chapters()

        self.add_toc()
        self.book.add_item(epub.EpubNcx())
        self.book.add_item(epub.EpubNav())

        self.book.spine = self.book.items

        epub.write_epub(self.outfile_name, self.book, epub_options)

    def add_chapters(self):
        for chapter in self.epub_chapters():
            self.book.add_item(chapter)

    def add_cover(self):
        self.book.set_cover("cover_image.svg", self.story.cover_svg)

    def add_info_page(self):
        page = epub.EpubHtml(uid="info_page", title="info page", file_name="info.xhtml")
        page.content = f"{self.story.title}<br>by {self.story.author_name}"
        self.book.add_item(page)

    def add_toc(self):
        self.book.toc = tuple(chapter for chapter in self.epub_chapters())

    @functools.lru_cache()
    def build_epub_html(self, chapter, num):
        file_name = f"chap_{num:03}.xhtml"
        epub_html = epub.EpubHtml(title=chapter.title, file_name=file_name, lang="en")
        epub_html.content = self.text_for_chapter(chapter)
        return epub_html

    @functools.lru_cache()
    def text_for_chapter(self, chapter):
        if len(self.story.chapters) > 1:
            return f"{chapter.title}\n\n{chapter.text}"
        else:
            return chapter.text

    @functools.lru_cache()
    def epub_chapters(self):
        return [
            self.build_epub_html(chapter, num)
            for num, chapter in enumerate(self.story.chapters)
        ]
