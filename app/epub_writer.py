from ebooklib import epub
import functools

from app.markdown_parser import MarkdownParser


class EpubWriter:
    def __init__(self, story, outfile_name):
        self.story = story
        self.book = epub.EpubBook()
        self.outfile_name = outfile_name

    def write_epub(self):
        self.book.set_title(self.story.title)
        self.book.set_language("en")

        self.book.add_author(self.story.author_name)
        #self.story.date_start  # TODO decide which should be the publish date
        #self.story.date_end

        self.add_chapters()

        self.add_toc()
        self.book.add_item(epub.EpubNcx())

        self.book.spine = ["nav"] + self.book.items

        epub.write_epub(self.outfile_name, self.book)

    def add_chapters(self):
        for chapter in self.epub_chapters():
            self.book.add_item(chapter)

    def add_toc(self):
        self.book.toc = tuple(chapter for chapter in self.epub_chapters())

    @functools.lru_cache()
    def build_epub_html(self, chapter, num):
        file_name = f"chap_{num:03}.xhtml"
        epub_html = epub.EpubHtml(title=chapter.title, file_name=file_name, lang="en")
        epub_html.content = MarkdownParser(chapter.text).as_html()
        return epub_html

    @functools.lru_cache()
    def epub_chapters(self):
        return [self.build_epub_html(chapter, num)
                for num, chapter
                in enumerate(self.story.chapters)]
